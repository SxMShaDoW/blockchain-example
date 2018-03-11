from user import User
from ledger import Ledger
import random
from cryptohash import cryptohash


class Miner(User):
    """
    A user that can mine on the blockchain
    """
    def last_block_hash(self):
        """ Generate a cryptohash of the last block """
        max_nonce_attempts = 1000000
        difficulty = 4
        msg = self._ledger.all_transactions[self._ledger.block_count - 1]['hdr']
        return cryptohash(msg, max_nonce_attempts, difficulty)

    def do_work(self, mining_reward):
        """ Mine a block if it is full and reward the miner """
        try:
            if self._ledger.is_block_full():
                self.create_new_block()
                # reward the miner from the system pool as the first transaction on the new block
                self._ledger.add_transaction('Anon', self.name(), mining_reward)
            else:
                raise
        except Exception as e:
                logger.exception('Unable to determine if block is full')   

    def is_valid_block_chain(self):
        """
        Check all the headers of the blockchain to make sure it hasn't been tampered with
        """
        max_nonce_attempts = 1000000
        difficulty = 4
        for i, transaction in enumerate(self._ledger.all_transactions):
            try:
                if i == 0:
                    continue
                current_block = transaction['hdr']
                previous_block = self._ledger.all_transactions[i - 1]['hdr']
                nonce, hash_hex = cryptohash(previous_block, max_nonce_attempts, difficulty)
                if nonce != current_block['rand'] and hash_hex != current_block['previous_hash']:
                    print('Warning blockchain may be tampered')
                    break
                else:
                    raise
            except Exception as e:
                logger.exception('Unable to determine if blackchain has been tampered with')
        return True

    def create_new_block(self):
        """ Create a new block """
        self._ledger.block_count += 1
        self._ledger.next_block = 'block_' + str(self._ledger.block_count) + '.json'
        self._ledger.all_transactions[self._ledger.block_count - 1]['next_block'] = self._ledger.next_block
        nonce, hash_hex = self.last_block_hash()
        new_block_header = {"Miner": self.name(), "previous_hash": hash_hex, "rand": nonce}
        self._ledger.all_transactions.append({"transactions": [], "next_block": '', "hdr": new_block_header})
