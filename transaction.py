import datetime


# Represents a transaction
class Transaction:
    def __init__(self):
        self.acc_number = ""
        self.type = ""
        self.date: datetime = None
        self.amount = 0

    def toCSVFormat(self):
        datestr = self.date.strftime('%m-%d-%Y')
        data = [datestr, '', '', '', self.type, '', '', self.acc_number, '', '', str(self.amount)]
        return ','.join(data)