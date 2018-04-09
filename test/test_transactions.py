import unittest

from itertools import groupby

from transactions.transactions import Transaction, Transactions
from data.data import transactions_response, response

transaction_data = [
    Transaction('2013-12-22', '-110.71'),
    Transaction('2013-12-22', '-10.22'),
    Transaction('2013-05-13', '117.53'),
    Transaction('2013-03-19', '-60.90')
]

reduced_data = [
    ['2013-03-19', '-60.90'],
    ['2013-05-13', '117.53'],
    ['2013-12-22', '-120.93']
]


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
        self.transactions.add_transactions(transaction_data)
        self.assertEqual(
            len(self.transactions.transactions), len(transaction_data))

    def test_process_response(self):
        self.transactions._process_response('', response)
        self.assertEqual(
            len(self.transactions.transactions),
            len(response['transactions']))

    def test_validate_data_valid(self):
        self.assertTrue(self.transactions._validate_data(response))

    def test_validate_data_no_page(self):
        self.assertFalse(self.transactions._validate_data({
            "totalCount": 38,
            "transactions": []
        }))

    def test_validate_data_no_count(self):
        self.assertFalse(self.transactions._validate_data({
            "page": 1,
            "transactions": []
        }))

    def test_validate_data_no_transactions(self):
        self.assertFalse(self.transactions._validate_data({
            "totalCount": 38,
            "page": 1,
        }))

    def test_serialize_transactions(self):
        transactions = self.transactions \
                           ._serialize_transactions(transactions_response)

        for transaction, item in zip(transactions, transactions_response):
            self.assertEqual(transaction.date, item['Date'])
            self.assertEqual(transaction.amount, float(item['Amount']))
        self.assertEqual(len(transactions), len(transactions_response))

    def test_serialize_transactions_empty(self):
        self.assertEqual(len(self.transactions._serialize_transactions([])), 0)

    def test_sum_transactions(self):
        self.transactions.add_transactions(transaction_data)
        self.assertEqual(
            self.transactions.sum_transactions(),
            sum(item.amount for item in transaction_data))

    def test_sum_transactions_empty(self):
        self.assertEqual(self.transactions.sum_transactions(), 0)

    def test_reduce_transactions(self):
        sorted_transactions = sorted(transaction_data, key=lambda x: x.date)
        grouped_transactions = groupby(sorted_transactions, lambda x: x.date)
        transactions = self.transactions \
                           ._reduce_transactions(grouped_transactions)
        for transaction, item in zip(transactions, reduced_data):
            self.assertEqual(transaction[0], item[0])
            self.assertEqual('{0:.2f}'.format(transaction[1]), item[1])

    def calculate_running_balances(self):
        self.transactions.add_transactions(transaction_data)
        transactions = self.transactions.calculate_running_balances()
        for transaction, item in zip(transactions, reduced_data):
            self.assertEqual(transaction[0], item[0])
            self.assertEqual('{0:.2f}'.format(transaction[1]), item[1])


if __name__ == '__main__':
    unittest.main()
