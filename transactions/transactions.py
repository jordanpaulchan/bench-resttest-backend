import requests

from itertools import groupby


class Transaction(object):
    def __init__(self, date, amount):
        self.date = date
        self.amount = float(amount)


class Transactions(object):
    def __init__(self):
        self.transactions = []

    def add_transactions(self, transactions):
        """ Add transactions to the instance """

        self.transactions.extend(transactions)

    def fetch_transactions(self, url, page=1):
        """ Given a url, fetch all of the transactions on all of the pages """

        request_url = '{}/{}.json'.format(url, page)
        try:
            req = requests.get(request_url, timeout=10)
        except Exception as e:
            # TODO: handle exceptions
            print 'Request Failed'
        else:
            self._validate_response(url, req)

    def sum_transactions(self):
        """ Calculates the sum of all of the transactions """

        return sum(transaction.amount for transaction in self.transactions)

    def calculate_running_balances(self):
        """ Calculates the running balances of the transactions """

        # Sort the transactions
        sorted_transactions = sorted(self.transactions, key=lambda x: x.date)

        # Group the transactions
        grouped_transactions = groupby(sorted_transactions, lambda x: x.date)

        # Return the sum of the group transactions
        return self._reduce_transactions(grouped_transactions)

    def _validate_response(self, url, response):
        """ Validate the status code of the response """

        if not response.status_code == 200:
            # TODO: handle non 200 case
            return None

        try:
            data = response.json()
        except Exception as e:
            # TODO: handle json exceptions
            print 'Failed to parse json'
        else:
            self._process_response(url, data)

    def _process_response(self, url, response):
        """ Save the transactions and recursively call the next page """

        if not self._validate_data(response):
            # TODO: handle invalid data
            return None

        self.add_transactions(
            self._serialize_transactions(response['transactions']))

        # If not on the last page recursively request the next page
        if response['page'] < response['totalCount']:
            self.fetch_transactions(url, response['page'] + 1)

    def _validate_data(self, data):
        """ Validate the data response """

        keys = ['page', 'totalCount', 'transactions']
        return all(key in data for key in keys)

    def _serialize_transactions(self, transactions):
        """ Serialize the data and create transaction objects """

        return [
            Transaction(item['Date'], item['Amount'])
            for item in transactions
        ]

    def _reduce_transactions(self, transactions):
        """ Reduce all of the transactions for each date """

        return [
            [date, sum(item.amount for item in items)]
            for date, items in transactions
        ]
