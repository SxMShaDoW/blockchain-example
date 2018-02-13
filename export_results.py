from tranGen import transaction_generator
import json

monies, users = transaction_generator()


def generate_all_transactions_json(transactions):
    """ Iterate through all transactions to export into jsons by block """
    
    for i, transaction in enumerate(transactions):
        file_name = 'block_' + str(i) + '.json'
        with open(file_name, 'w') as results:
            json.dump(transaction, results)


def generate_all_transactions_by_user_json(transactions):
    """ Dump all the transaction per user data into a json """
    file_name = 'transactions_per_user.json'
    with open(file_name, 'w') as results:
        json.dump(transactions, results)

generate_all_transactions_json(monies.all_transactions)
generate_all_transactions_by_user_json(monies.transactions_by_user)
