import random
from ledger import Ledger
from user import User
from miner import Miner
import time
from tranGen import create_users_and_ledger, generate_initial_balance, generate_transactions_on_ledger, mine_blocks_on_ledger


def test_create_users_and_ledger():
    """ test the transaction generator """

    ledger, anon, users, miners = create_users_and_ledger()
    assert isinstance(ledger, Ledger)
    assert isinstance(anon, User)
    for user in users:
        assert isinstance(user, User)
    for miner in miners:
        assert isinstance(miner, Miner)


def test_generate_initial_balance():
    """ test to make sure initial balance is on a user """
    # Setup
    mock_ledger = Ledger('foo')
    mock_anon = User('Anon', mock_ledger)
    mock_user = User('bar', mock_ledger)
    mock_users = [mock_user]
    initial_value = 1000
    generate_initial_balance(mock_anon, mock_users, initial_value, 10)
    assert mock_anon._credit == initial_value * len(mock_users) * 10


def test_generate_transactions_on_ledger():
    """ test generating transactions """
    # Setup
    mock_ledger = Ledger('foo')
    mock_anon = User('Anon', mock_ledger)
    mock_user = User('bar', mock_ledger)
    mock_user_2 = User('foobar', mock_ledger)
    mock_miner = Miner('foominer', mock_ledger)
    mock_users = [mock_user, mock_user_2]
    mock_miners = [mock_miner]
    initial_value = 100
    generate_initial_balance(mock_anon, mock_users, initial_value, 10)
    ledger, users = generate_transactions_on_ledger(
        mock_ledger, mock_users, 3, mock_miners, 10)
    assert isinstance(ledger, Ledger)
    for user in users:
        assert isinstance(user, User)


def test_mine_blocks_on_ledger(monkeypatch):
    """ test mining blocks """
    mock_ledger = Ledger('foo')
    mock_miner = Miner('foominer', mock_ledger)
    mock_miner_2 = Miner('barminer', mock_ledger)
    mock_miners = [mock_miner, mock_miner_2]
    mock_ledger.transaction_sequence = 256
    mine_blocks_on_ledger(mock_ledger, mock_miners, 10)
