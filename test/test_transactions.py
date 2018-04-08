import unittest

from transactions.transactions import Transaction, Transactions
from data.data import transaction_data, transactions_response, response


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


if __name__ == '__main__':
    unittest.main()
