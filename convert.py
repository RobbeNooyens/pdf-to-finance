import datetime

import PyPDF2
import re

# Const Regex patterns
from transaction import Transaction

start_pattern_inline = re.compile(r'.*\d{3}\s\d{2}-\d{2}-\d{4}\s\d{2}-\d{2}\s[\d,]+\s[+\-]')
start_pattern = re.compile(r'\d{3}\s\d{2}-\d{2}-\d{4}\s\d{2}-\d{2}\s[\d,]+\s[+\-]')
ignore_pattern = re.compile(r'^(Saldo|KBC\sBank\sNV)')
account_pattern = re.compile(r'^(BE|DE|NL|FR)\d{2}')


def convert(filename):
    # Convert PDF to TXT file
    with open(filename + ".txt", "w") as output:
        with open(filename + ".pdf", 'rb') as pdf:
            # create reader variable that will read the pdffileobj
            pdfreader = PyPDF2.PdfFileReader(pdf)
            for page in pdfreader.pages:
                output.writelines(page.extractText())

    # Extract useful information
    splitted = []
    with open(filename + ".txt") as file:
        transaction = []
        current_transaction = False
        for line in file:
            line = line.replace("\n", "")
            if start_pattern_inline.match(line):
                if transaction:
                    splitted.append(transaction)
                transaction = [start_pattern.search(line).group(0)]
                current_transaction = True
            elif ignore_pattern.match(line):
                current_transaction = False
            else:
                if current_transaction:
                    transaction.append(line)

    # Create Transaction objects based on transaction information
    transactions = []
    for transaction_info in splitted:
        transaction = Transaction()
        line1 = transaction_info[0]  # Nr. Date Valuta Amount Credit/Debit
        transaction.type = transaction_info[1]  # Transaction type
        line3 = transaction_info[2]  # BExxxxxxxxx
        assert start_pattern.match(line1)
        transaction.acc_number = line3 if account_pattern.match(line3) else ""
        line1_data = line1.split(" ")
        assert len(line1_data) == 5
        transaction.amount = float((line1_data[4]) + line1_data[3].replace(",", "."))
        transaction.date = datetime.datetime.strptime(line1_data[1], '%d-%m-%Y')
        transactions.append(transaction)

    # Convert Transaction objects to CSV format
    with open(filename + ".csv", 'w') as file:
        for transaction in transactions:
            file.write(transaction.toCSVFormat())
            file.write("\n")