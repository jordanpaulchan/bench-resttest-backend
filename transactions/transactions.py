import requests


class Transaction(object):
    def __init__(self, date, amount):
        self.date = date
        self.amount = float(amount)


class Transactions(object):
    def __init__(self):
        self.transactions = []

    def add_transactions(self, transactions):
        self.transactions.extend(transactions)

    def fetch_transactions(self, url, page=1):
        request_url = '{}/{}.json'.format(url, page)
        try:
            req = requests.get(request_url, timeout=10)
        except Exception as e:
            # TODO: handle exceptions
            print 'Request Failed'
        else:
            self._validate_response(url, req)

    def _validate_response(self, url, response):
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
        if not self._validate_data(response):
            # TODO: handle invalid data
            return None

        self.add_transactions(
            self._serialize_transactions(response['transactions']))

        # If not on the last page recursively request the next page
        if response['page'] <= response['totalCount']:
            self.fetch_transactions(url, response['page'] + 1)

    def _validate_data(self, data):
        keys = ['page', 'totalCount', 'transactions']
        return all(key in data for key in keys)

    def _serialize_transactions(self, transactions):
        return [
            Transaction(item['Date'], item['Amount'])
            for item in transactions
        ]
