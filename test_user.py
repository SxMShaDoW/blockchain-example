from user import User
from ledger import Ledger
from pytest import raises


def test_is_balance_gt_0():
    """ Test the is balance greater than 0 function """
    # Setup
    ledger_1 = Ledger('monies')
    user_2 = User('foo', ledger_1)
    user_1 = User('Anon', ledger_1)
    amount = 1

    # test base case for Anon
    user_1._credit = 100
    result = user_1.is_balance_gt_0(amount)
    assert result == True

    # test send amount for users
    amount = 101
    ledger_1.transactions_by_user['foo']['running_balance'] = []
    ledger_1.transactions_by_user['foo']['running_balance'].append(-101)
    assert user_2.is_balance_gt_0(amount) == True
    # test when user doesn't have enough money
    ledger_1.transactions_by_user['foo']['running_balance'].append(-102)
    assert user_2.is_balance_gt_0(amount) == False

    # test exception case
    ledger_1.transactions_by_user = Exception
    with raises(Exception):
        user_2.is_balance_gt_0(amount)


def test_send_exception():
    """ Test if send will throw an exception if no monies """
    # Setup
    ledger_1 = Ledger('monies')
    user_2 = User('foo', ledger_1)
    user_1 = User('oops', ledger_1)
    amount = 1
    with raises(Exception):
        user_1.send(amount, user_2)
