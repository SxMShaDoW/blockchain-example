import collections
import math
from statistics import median, mean


class Ledger(object):
    """ A ledger class that can add or cancel transactions on a blockchain """
    def __init__(self, name):
        self.name = name
        self._block_limit = 256
        self.transaction_confirmed_count = 0
        self.transaction_cancelled_count = 0
        self.transaction_sequence = 0
        self.block_count = 0
        self.all_transactions = []
        self.all_transactions.append({"transactions": [], "next_block": '', "hdr": {}})
        self.next_block = 'block_' + str(self.block_count) + '.json'
        self.transaction_cancelled_tids = []
        self.transaction_values_with_cancels = []
        self.transaction_values = []
        self.transactions_by_user = collections.defaultdict(dict)

    def is_block_full(self):
        """
        If the next sequence number is divisble by the block limit
        and isn't the first transaction
        then create a new block
        """
        return self.transaction_sequence % self._block_limit == 0 and self.transaction_sequence != 0

    def initialize_user_data(self, user):
        """ Initialize user data we are keeping track of """
        self.transactions_by_user[user]['sent_transactions'] = 0
        self.transactions_by_user[user]['sent_totals'] = 0
        self.transactions_by_user[user]['received_transactions'] = 0
        self.transactions_by_user[user]['received_totals'] = 0
        self.transactions_by_user[user]['running_balance'] = []

    def record_transaction_per_user(self, sender, recipient, amount):
        """ Keep track of important user specific information so we can report on it """
        if sender not in self.transactions_by_user:
            self.initialize_user_data(sender)
        if recipient not in self.transactions_by_user:
            self.initialize_user_data(recipient)
        # add to the sender totals
        self.transactions_by_user[sender]['sent_transactions'] += 1
        self.transactions_by_user[sender]['sent_totals'] += amount
        sender_balance = self.transactions_by_user[sender]['running_balance']
        if len(sender_balance) == 0:
            self.transactions_by_user[sender]['running_balance'].append(-amount)
        else:
            # get the last balance and subtract the amount from the running total
            sender_current_balance = self.transactions_by_user[sender]['running_balance'][-1]
            self.transactions_by_user[sender]['running_balance'].append(sender_current_balance - amount)
        # add to the recipient totals
        self.transactions_by_user[recipient]['received_transactions'] += 1
        self.transactions_by_user[recipient]['received_totals'] += amount
        receiver_balance = self.transactions_by_user[recipient]['running_balance']
        if len(receiver_balance) == 0:
            self.transactions_by_user[recipient]['running_balance'].append(amount)
        else:
            # get the last balance and add the amount to the running total
            receiver_current_balance = self.transactions_by_user[recipient]['running_balance'][-1]
            self.transactions_by_user[recipient]['running_balance'].append(receiver_current_balance + amount)

    def record_highest_lowest_balance(self, user):
        """ Record the highest and lowest balance of a user """
        running_balance = self.transactions_by_user[user]['running_balance']
        # since there is only 1 amount, it must be the highest / lowest
        if len(running_balance) == 1:
            self.transactions_by_user[user]['highest_balance'] = running_balance[0]
            self.transactions_by_user[user]['lowest_balance'] = running_balance[0]
        # if there is more than 1 transaction, determine the new highest / lowest
        elif len(running_balance) > 1:
            user_new_highest = max(running_balance)
            self.transactions_by_user[user]['highest_balance'] = user_new_highest

            user_new_lowest = min(running_balance)
            self.transactions_by_user[user]['lowest_balance'] = user_new_lowest

    def add_transaction(self, sender, recipient, amount):
        """
        Adds a transaction to a ledger
        It takes in a user object as sender
        it takes in a user object as recipient
        it takes in an integer as an amount
        """
        # create a dictionary for a transaction
        transaction = {}
        transaction['tid'] = self.transaction_sequence
        transaction['sender'] = sender
        transaction['recipient'] = recipient
        transaction['amount'] = amount
        # add the transaction to the ledger in the correct place
        self.all_transactions[self.block_count]['transactions'].append(transaction)
        # confirming transaction
        self.transaction_confirmed_count += 1
        # increment the unique tid
        self.transaction_sequence += 1
        # keep track of the value total added
        self.transaction_values.append(amount)
        # keep track of the entire flow of money (including cancels)
        self.transaction_values_with_cancels.append(amount)
        self.record_transaction_per_user(sender, recipient, amount)
        self.record_highest_lowest_balance(sender)
        self.record_highest_lowest_balance(recipient)

    def refund_transaction(self, tid):
        """
        Refund the money to the users if a transaction is cancelled
        """
        # find the cancelled tid block
        cancelled_tid_block = math.floor(tid // self._block_limit)

        # find the cancelled transaction using the cancelled tid
        cancelled_amount = self.all_transactions[cancelled_tid_block]['transactions'][tid % self._block_limit]['amount']
        sender_refund_name = self.all_transactions[cancelled_tid_block]['transactions'][tid % self._block_limit]['sender']
        receiver_refund_name = self.all_transactions[cancelled_tid_block]['transactions'][tid % self._block_limit]['recipient']

        # remove from sender totals
        self.transactions_by_user[sender_refund_name]['sent_transactions'] -= 1
        self.transactions_by_user[sender_refund_name]['sent_totals'] -= cancelled_amount

        # update running balance for sender
        sender_current_balance = abs(self.transactions_by_user[sender_refund_name]['running_balance'][-1])
        self.transactions_by_user[sender_refund_name]['running_balance'].append(sender_current_balance + cancelled_amount)

        # remove from receiver
        self.transactions_by_user[receiver_refund_name]['received_transactions'] -= 1
        self.transactions_by_user[receiver_refund_name]['received_totals'] -= cancelled_amount

        # update running balance for receiver
        receiver_current_balance = abs(self.transactions_by_user[receiver_refund_name]['running_balance'][-1])
        self.transactions_by_user[receiver_refund_name]['running_balance'].append(receiver_current_balance - cancelled_amount)

        # keep a running list of cancelled amounts
        self.transaction_values_with_cancels.append(-cancelled_amount)
        # remove it from the running list of confirmed transactions
        if cancelled_amount in self.transaction_values:
            self.transaction_values.remove(cancelled_amount)

    def is_cancellable(self, tid):
        """
        Determine if the tid can be cancelled based on the following rules
        1. Transaction can't already be cancelled
        2. Transaction can't cancel itself
        3. Transaction can't be a mining reward
        """
        return tid not in self.transaction_cancelled_tids \
                and tid < self.transaction_sequence \
                and tid % self._block_limit != 0 # first transaction

    def cancel_transaction(self, tid):
        """
        Cancel a transaction based on a tid
        """
        transaction = {}
        transaction['tid'] = self.transaction_sequence
        transaction['cancelled_tid'] = tid
        # check if the transaction has already been cancelled
        # check that the transaction isn't trying to cancel itself
        if self.is_cancellable(tid):
            # adding the transaction to the ledger
            self.all_transactions[self.block_count]['transactions'].append(transaction)
            # keep track of cancelled tids
            self.transaction_cancelled_tids.append(self.transaction_sequence)
            # confirming transaction
            self.transaction_cancelled_count += 1
            # incrementing the unique tid
            self.transaction_sequence += 1
            # refund the money to the correct user
            self.refund_transaction(tid)

    def total_transactions(self):
        """ Return the total confirmed and cancelled transactions """
        return self.transaction_confirmed_count + self.transaction_cancelled_count

    def net_value(self):
        """ Return the net value of a Ledger """
        if len(self.transaction_values) > 0:
            return sum(self.transaction_values)
        else:
            return 0

    def median_value(self):
        """ Return the median transaction value from the ledger """
        if len(self.transaction_values) > 0:
            return median(sort(self.transaction_values))
        else:
            return 0

    def average_value(self):
        """ Return the average transaction value on the ledger """
        if len(self.transaction_values) > 0:
            return mean(self.transaction_values)
        else:
            return 0

    def total_confirmed_transactions(self):
        """ Return the total confirmed transactions count """
        return self.transaction_confirmed_count

    def total_cancelled_transactions(self):
        """ Return the total cancalled transactions count """
        return self.transaction_cancelled_count
