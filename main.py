import datetime

import PyPDF2
import re

# Define patterns for text manipulation
from Transaction import Transaction

start_pattern = re.compile(r'\d{3}\s\d{2}-\d{2}-\d{4}\s\d{2}-\d{2}\s[\d,]+\s[+\-]')
ignore_pattern = re.compile(r'^(Saldo|KBC\sBank\sNV)')
account_pattern = re.compile(r'^(BE|DE|NL|FR)\d{2}')

# Convert PDF to TXT file
with open(r"out.txt", "w") as output:
    with open('Test.pdf', 'rb') as pdf:
        # create reader variable that will read the pdffileobj
        pdfreader = PyPDF2.PdfFileReader(pdf)
        for page in pdfreader.pages:
            output.writelines(page.extractText())

# Extract useful information
splitted = []
with open("out.txt") as file:
    transaction = []
    current_transaction = False

    for line in file:
        line = line.replace("\n", "")
        if start_pattern.match(line):
            if transaction:
                splitted.append(transaction)
            transaction = [line]
            current_transaction = True
        elif ignore_pattern.match(line):
            current_transaction = False
        else:
            if current_transaction:
                transaction.append(line)
    #
    # for trans in splitted:
    #     print("========================")
    #     for line in trans:
    #         print(line)

transactions = []
for transaction_info in splitted:
    transaction = Transaction()
    line1 = transaction_info[0] # Nr. Date Valuta Amount Credit/Debit
    line2 = transaction_info[1] # Transaction type
    line3 = transaction_info[2] # BExxxxxxxxx
    assert start_pattern.match(line1)
    transaction.acc_number = line3 if account_pattern.match(line3) else ""
    line1_data = line1.split(" ")
    assert len(line1_data) == 5
    transaction.amount = float((line1_data[4]) + line1_data[3].replace(",", "."))
    transaction.date = datetime.datetime.strptime(line1_data[1], '%d-%m-%Y')
    transactions.append(transaction)

with open("transactions.csv", 'w') as file:
    for transaction in transactions:
        file.write(transaction.toCSVFormat())
        file.write("\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass

