# CakeToAccointing
Rudimentary code to transform cake transaction report to accointing format. In the current version, only the staking rewards are considered.

If not already done, install the python virtualenv tool with
`pip install virtualenv`

Initialize the virtual environment 
`virtualenv venv`

Activate the virtual environment
`source venv/bin/activate`

Test with the sample file:
`python transformCakeTransaction.py <infile> <outfile>`

You can run the script with the provided test file
`python transformCakeTransactions.py tests/test_cake.csv.txt accointing_out.csv`
This will generate the file accointing_out.csv which can be uploaded. Please note, that only the staking rewards are taken into account at the moment.

You can display more information with `transformCakeTransaction.py -h`
