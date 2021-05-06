import argparse
import os.path
import csv
import datetime as dt


def print_header(csv_content, num_of_rows):
    print(csv_content[0:num_of_rows])


def convert_datetime_cake_to_accointing(cake_datetime):
    ts = dt.datetime.fromisoformat(cake_datetime)
    return (ts + ts.utcoffset()).strftime("%m/%d/%Y %H:%M:%S")


def convert_operation_to_accointing(cake_operation):
    cake2accointing = {"Staking reward": "staked", "Bonus/Airdrop": "airdrop", "Swapped out": "remove funds",
                       "Swapped in": "add funds", "Deposit": "add funds", "Withdrawal": "withdrawal",
                       "Withdrawal fee": "fee"}
    return cake2accointing[cake_operation]


def get_accointing_header():
    header_row = [
        "transactionType",
        "date",
        "inBuyAmount",
        "inBuyAsset",
        "outSellAmount",
        "outSellAsset",
        "feeAmount (optional)",
        "feeAsset (optional)",
        "classification (optional)",
        "operationId (optional)"
    ]
    return header_row


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="provide path to input file")
    parser.add_argument("outfile", help="provide path to output file")
    parser.add_argument("-f", "--force_overwrite", help="overwrite outfile if already exists", action="store_true")

    args = parser.parse_args()

    print("Trying to convert Cake transactions into Accointing format...")
    print("Input file is:", args.infile)
    print("Output file will be:", args.outfile)

    infile = args.infile
    outfile = args.outfile

    if args.force_overwrite:
        print("overwrite enabled")
        overwrite = True
    else:
        overwrite = False

    if not overwrite:
        if os.path.isfile(outfile):
            raise Exception(outfile, "exists but overwrite is not enabled. Try using the -f option.")

    try:
        with open(args.infile) as f:
            with open(infile, newline='') as f:
                cakeCSV = list(csv.reader(f))
    except IOError:
        print("File is not accessible")
        raise

    print(f'Cake import looks like:')
    print_header(cakeCSV, 2)

    # remove cake csv header
    cakeCSV.pop(0)

    with open(outfile, "w", newline='') as accointingCSV:
        writer = csv.writer(accointingCSV, delimiter=',')
        writer.writerow(get_accointing_header())
        for row in cakeCSV:
            if row[1] == 'Staking reward':
                transactionType = 'deposit'
                timestamp = convert_datetime_cake_to_accointing(row[0])
                inBuyAmount = row[2]
                inBuyAsset = row[3]
                outSellAmount = ''
                outSellAsset = ''
                feeAmount = ''
                feeAsset = ''
                classification = convert_operation_to_accointing(row[1])
                operationID = ''

                accointing_row = [
                    transactionType,
                    timestamp,
                    inBuyAmount,
                    inBuyAsset,
                    outSellAmount,
                    outSellAsset,
                    feeAmount,
                    feeAsset,
                    classification,
                    operationID
                ]
                writer.writerow(accointing_row)
