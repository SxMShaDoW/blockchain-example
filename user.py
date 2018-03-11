#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


class User(object):

    """ A user class that can send and receive money on a ledger """

    def __init__(self, name, ledger):
        self._name = name
        self._credit = 0  # used to populate the first user
        self._ledger = ledger

    def send(self, amount, recipient):
        """ Send money on the ledger if the user has enough to send """

        try:
            if self.is_balance_gt_0(amount):
                # add to the ledger
                self._ledger.add_transaction(
                    self.name(), recipient.name(), amount)
        except Exception as e:
            logger.exception(
                'Unable to determine if user has enough monies to send')
            raise e

    def is_balance_gt_0(self, amount):
        """ Return true if the current balance is greater than 0 """

        try:
            # if you are the Anon account, you are okay
            if self._credit - amount > 0 and self.name() == 'Anon':
                return True
            # if you have enough money to send you are okay
            elif self._ledger.transactions_by_user[self.name()]['running_balance'][-1] + amount >= 0:
                return True
            else:
                return False
        except Exception as e:
            logger.exception('Ledger does not have a running balance for user')
            raise e

    def increase_credit(self, amount):
        """ Increase the credit of a user """

        # this is only used for the Anon account
        self._credit += amount

    def name(self):
        """ Return the name of the user """

        return self._name

    def total_credit(self):
        """ Return the total credit a user has / received """

        return self._ledger.transactions_by_user[self.name()]['received_totals']

    def total_debit(self):
        """ Return the total debit / money owed for a user """

        return self._ledger.transactions_by_user[self.name()]['sent_totals']

    def total_value(self):
        """ Return the balance for a user """

        sent = self._ledger.transactions_by_user[self.name()]['sent_totals']
        received = self._ledger.transactions_by_user[self.name(
        )]['received_totals']
        return sent - received

    def total_transaction(self):
        """ Return the total transactions a user was involved with """

        sent_total = self._ledger.transactions_by_user[self.name(
        )]['sent_transactions']
        received_total = self._ledger.transactions_by_user[self.name(
        )]['received_transactions']
        return sent_total + received_total

    def total_credit_transaction(self):
        """ Return the total transactions a user received """

        return self._ledger.transactions_by_user[self.name()]['received_transactions']

    def total_debit_transaction(self):
        """ Return the total sent transactions for a user """

        return self._ledger.transactions_by_user[self.name()]['sent_transactions']
