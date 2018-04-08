class Transaction(object):
    def __init__(self, date, amount):
        self.date = date
        self.amount = float(amount)


class Transactions(object):
    def __init__(self):
        self.transactions = []

    def add_transactions(self, transactions):
        self.transactions.extend(transactions)
