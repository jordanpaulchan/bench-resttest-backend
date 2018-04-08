import unittest

from transactions.transactions import Transaction, Transactions
from data.transactions_data import transactions_data


class TransactionTests(unittest.TestCase):
    def setUp(self):
        super(TransactionTests, self).setUp()
        self.transaction = Transaction('2013-12-22', '-110.71')

    def tearDown(self):
        super(TransactionTests, self).tearDown()
        self.transaction = None

    def test_init(self):
        self.assertEqual(self.transaction.date, '2013-12-22')
        self.assertEqual(self.transaction.amount, -110.71)


class TransactionsTests(unittest.TestCase):
    def setUp(self):
        super(TransactionsTests, self).setUp()
        self.transactions = Transactions()

    def tearDown(self):
        super(TransactionsTests, self).tearDown()
        self.transactions = None

    def test_init(self):
        self.assertEqual(self.transactions.transactions, [])

    def test_add_transactions(self):
        self.transactions.add_transactions(transactions_data)
        self.assertEqual(
            len(self.transactions.transactions), len(transactions_data))


if __name__ == '__main__':
    unittest.main()
