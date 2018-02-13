from tranGen import transaction_generator
from statistics import mean
import glob
import json


class In_Memory_Report():
    """ Report class for querying the ledger in memory """
    def __init__(self, name):
        self._name = name

    @classmethod
    def total_transactions(cls, ledger):
        """ Print the total transactions for a specified ledger """
        print(f'Total transactions for {ledger.name}: {ledger.total_transactions()}')

    @classmethod
    def total_cancelled_transactions(cls, ledger):
        """ Print the total cancelled transactions for a specified ledger """
        print(f'Total cancelled transactions for {ledger.name}: {ledger.total_cancelled_transactions()}')

    @classmethod
    def total_transactions_per_user(cls, ledger):
        """ Print the total cancelled transactions per user a specified ledger """
        transaction_data = ledger.transactions_by_user
        for user in ledger.transactions_by_user:
            sent_transactions = transaction_data[user]['sent_transactions']
            received_transactions = transaction_data[user]['received_transactions']
            total_transactions = sent_transactions + received_transactions
            print(f'Total transactions for {user} : {total_transactions}')

    @classmethod
    def total_credits_per_user(cls, ledger):
        """ Print the total credits per user a specified ledger """
        transaction_data = ledger.transactions_by_user
        for user in ledger.transactions_by_user:
            received_totals = transaction_data[user]['received_totals']
            print(f'Total credits for {user} : {received_totals}')

    @classmethod
    def total_debits_per_user(cls, ledger):
        """ Print the total debits per user a specified ledger """
        transaction_data = ledger.transactions_by_user
        for user in ledger.transactions_by_user:
            sent_totals = transaction_data[user]['sent_totals']
            print(f'Total debits for {user} : {sent_totals}')

    @classmethod
    def highest_balance_per_user(cls, ledger):
        """ Print the highest balance per user a specified ledger """
        transaction_data = ledger.transactions_by_user
        for user in ledger.transactions_by_user:
            highest_balance = transaction_data[user]['highest_balance']
            print(f'Highest balance for {user} : {highest_balance}')

    @classmethod
    def lowest_balance_per_user(cls, ledger):
        """ Print the lowest balance per user a specified ledger """
        transaction_data = ledger.transactions_by_user
        for user in ledger.transactions_by_user:
            lowest_balance = transaction_data[user]['lowest_balance']
            print(f'Lowest balance for {user} : {lowest_balance}')

    @classmethod
    def total_money_exchanged(cls, ledger):
        """ Print the amount of money exchanged on a specified ledger """
        all_money = sum(ledger.transaction_values)
        print(f'Total money exchanged on {ledger.name} : {all_money}')

    @classmethod
    def average_transaction_value(cls, ledger):
        """ Print the average transaction value on a specified ledger """
        average_transaction = mean(ledger.transaction_values)
        print(f'Average transaction value on {ledger.name} : {average_transaction}')

    @classmethod
    def transactions(cls, ledger):
        """ Print the recorded transaction amounts on a specified ledger """
        transactions = ledger.transaction_values
        print(f'Transactions amount on {ledger.name} : {transactions}')

    @classmethod
    def transactions_with_cancels(cls, ledger):
        """ Print the transaction amounts on a specified ledger with cancelled transactions """
        transactions = ledger.transaction_values_with_cancels
        print(f'Transactions (with cancels) amount on {ledger.name} : {transactions}')

    @classmethod
    def all_transactions(cls, ledger):
        """ Print the transaction amounts on a specified ledger with cancelled transactions """
        transactions = ledger.all_transactions
        print(f'All transactions on the following ledger {ledger.name} : {transactions}')


class Report():
    """ Report class for reading .json files """
    def __init__(self, name):
        self._name = name

    @classmethod
    def load_all_transaction_files(cls):
        all_transactions = []
        for name in glob.glob('block_*.json'):
            with open(name, 'r') as f:
                datastore = json.load(f)
                all_transactions.append(datastore)
        return all_transactions

    @classmethod
    def load_all_data_per_user(cls):
        all_transactions_per_user = []
        for name in glob.glob('transactions_*.json'):
            with open(name, 'r') as f:
                datastore = json.load(f)
                all_transactions_per_user.append(datastore)
        return all_transactions_per_user

    @classmethod
    def total_transactions(cls, transactions):
        """ Print the total transactions for a specified ledger """
        count = 0
        for transaction in transactions:
            count += len(transaction['transactions'])
        print(f'Total transactions: {count}')

    @classmethod
    def total_cancelled_transactions(cls, transactions):
        """ Print the total cancelled transactions for a specified ledger """

        count = 0
        for transaction in transactions:
            for i in transaction['transactions']:
                if 'cancelled_tid' in i:
                    count += 1
        print(f'Total cancelled transactions for {count}')

    @classmethod
    def total_transactions_per_user(cls, data):
        """ Print the total cancelled transactions per user a specified ledger """
        data = data[0]
        for user in data:
            sent_transactions = data[user]['sent_transactions']
            received_transactions = data[user]['received_transactions']
            total_transactions = sent_transactions + received_transactions
            print(f'Total transactions for {user} : {total_transactions}')

    @classmethod
    def total_credits_per_user(cls, data):
        """ Print the total credits per user a specified ledger """
        data = data[0]
        for user in data:
            received_totals = data[user]['received_totals']
            print(f'Total credits for {user} : {received_totals}')

    @classmethod
    def total_debits_per_user(cls, data):
        """ Print the total debits per user a specified ledger """
        data = data[0]
        for user in data:
            sent_totals = data[user]['sent_totals']
            print(f'Total debits for {user} : {sent_totals}')

    @classmethod
    def highest_balance_per_user(cls, data):
        """ Print the highest balance per user a specified ledger """
        data = data[0]
        for user in data:
            highest_balance = data[user]['highest_balance']
            print(f'Highest balance for {user} : {highest_balance}')

    @classmethod
    def lowest_balance_per_user(cls, data):
        """ Print the lowest balance per user a specified ledger """
        data = data[0]
        for user in data:
            lowest_balance = data[user]['lowest_balance']
            print(f'Lowest balance for {user} : {lowest_balance}')

    @classmethod
    def total_money_exchanged(cls, data):
        """ Print the amount of money exchanged on a specified ledger """
        total = 0
        data = data[0]
        for user in data:
            sent_totals = data[user]['sent_totals']
            total += sent_totals
        print(f'Total money exchanged: {total}')

    @classmethod
    def average_transaction_value(cls, transactions):
        """ Print the average transaction value on a specified ledger """
        all_transaction_amounts = []
        for transaction in transactions:
            for i in transaction['transactions']:
                if 'amount' in i:
                    all_transaction_amounts.append(i['amount'])
        print(f'Average transaction value : {mean(all_transaction_amounts)}')


def createReport():
    report_2 = Report('Report from JSON')
    monies = report_2.load_all_transaction_files()
    data = report_2.load_all_data_per_user()
    report_2.total_transactions(monies)
    report_2.total_cancelled_transactions(monies)
    report_2.total_transactions_per_user(data)
    report_2.total_credits_per_user(data)
    report_2.total_debits_per_user(data)
    report_2.highest_balance_per_user(data)
    report_2.lowest_balance_per_user(data)
    report_2.total_money_exchanged(data)
    report_2.average_transaction_value(monies)

createReport()
