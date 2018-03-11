import ledger
import pytest


def test_is_block_full():
    """ test if a block is full """
    # Setup
    ledger_2 = ledger.Ledger('monies2')

    # test base case
    true_or_false = ledger_2.is_block_full()
    assert true_or_false == False

    # test if there are 256 transactions and limit is 256
    ledger_2.transaction_sequence = 256
    true_or_false = ledger_2.is_block_full()
    assert true_or_false == True

    # test if there are 255 transactions
    ledger_2.transaction_sequence = 255
    true_or_false = ledger_2.is_block_full()
    assert true_or_false == False


def test_is_cancellable():
    """ test if a transaction is cancellable """
    # Setup
    ledger_1 = ledger.Ledger('monies')
    tid_0 = 0
    ledger_1.transaction_cancelled_tids = [1, 5, 7]
    ledger_1.transaction_sequence = 100

    # Test when transaction doesn't exist
    true_or_false = ledger_1.is_cancellable(tid_0)
    assert true_or_false == False

    # test when transaction exists
    tid_3 = 3
    true_or_false = ledger_1.is_cancellable(tid_3)
    assert true_or_false == True

    # test when the transaction is itself
    tid_5 = 5
    ledger_1.transaction_sequence = 5
    true_or_false = ledger_1.is_cancellable(tid_5)
    assert true_or_false == False

    # test when the transaction is the first one
    tid_5 = 5
    ledger_1.transaction_sequence = 6
    ledger_1._block_limit = 0
    true_or_false = ledger_1.is_cancellable(tid_5)
    assert true_or_false == False


def test_median_value():
    """ Test transactions on ledger can return the median """
    # Setup
    ledger_1 = ledger.Ledger('monies')

    # test when no there are no values
    ledger_1.transaction_values = []
    assert ledger_1.median_value() == 0

    # test when it is odd
    ledger_1.transaction_values = [1, 5, 7]
    assert ledger_1.median_value() == 5

    # test sort and even numbers
    ledger_1.transaction_values = [1, 7, 6, 5]
    assert ledger_1.median_value() == 5.5
