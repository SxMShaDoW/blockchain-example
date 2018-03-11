from miner import Miner
from ledger import Ledger
from cryptohash import cryptohash


def test_last_block_hash():
    """
    Test function for last block hash
    """
    # Setup
    mock_ledger = Ledger('monies')
    mock_miner = Miner('Mock', mock_ledger)
    mock_header = {'hdr': 'foo'}
    mock_ledger.block_count = 1
    mock_ledger.all_transactions.append(mock_header)
    mock_message = mock_ledger.all_transactions[0]['hdr']
    mock_nonce_attempts = 1000000
    mock_difficulty = 4
    mock_hash = cryptohash(mock_message, mock_nonce_attempts, mock_difficulty)
    # Assert
    assert mock_miner.last_block_hash() == mock_hash
