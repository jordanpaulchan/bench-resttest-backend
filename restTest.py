from transactions.transactions import Transactions

URL = 'http://resttest.bench.co/transactions'

if __name__ == '__main__':
    transactions = Transactions()
    transactions.fetch_transactions(URL)

    print('Total Balance: {}'.format(transactions.sum_transactions()))

    print('Running Balances:')
    running_balances = transactions.calculate_running_balances()
    for date, balance in running_balances:
        print('{}: {}'.format(date, balance))
