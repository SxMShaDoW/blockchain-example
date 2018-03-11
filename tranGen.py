import random
from ledger import Ledger
from user import User
from miner import Miner
import time
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


def create_users_and_ledger():
    """ Create the users and ledger """
    monies = Ledger('monies')
    alice = User('Alice', monies)
    bob = Miner('Bob', monies)
    jon = User('Jon', monies)
    howard = User('Howard', monies)
    rocky = Miner('Rocky', monies)
    # using an anon user for creating an initial balance
    anon = User('Anon', monies)
    users = [alice, jon, howard]
    miners = [rocky, bob]
    return (monies, anon, users, miners)


def generate_initial_balance(donating_user, users, initial_balance, mining_reward):
    """ Generate the initial balance for each user on the ledger """
    donating_user.increase_credit(
        len(users) * initial_balance * mining_reward)
    for user in users:
        donating_user.send(initial_balance, user)


def generate_two_unique_users(users):
    """ Pick two unique users that aren't the same person """
    random_user_1 = random.choice(users)
    random_user_2 = random.choice(users)
    """ make sure the users aren't the same people """
    try:
        while random_user_2 == random_user_1:
            random_user_2 = random.choice(users)
        return (random_user_1, random_user_2)
    except Exception as e:
        logger.exception('there are no unique users')
        raise e


def generate_unique_cancelled_tid(users, trans_so_far, cancelled_transactions):
    """ Find a random transaction that hasn't been cancelled yet """
    # can't cancel the current one / self or the original starting balances
    random_cancel = random.randint(len(users), trans_so_far)
    while random_cancel in cancelled_transactions:
        random_cancel = random.randint(len(users), trans_so_far)
    return random_cancel


def generate_transactions_on_ledger(ledger, users, num_of_transactions, miners, mining_reward):
    """ Generate a ledger with given users and a set number of transactions """
    upper_bound_random_amount = 20
    for i in range(0, num_of_transactions):
        random_user_1, random_user_2 = generate_two_unique_users(users)
        cancelled_transactions_frequency = 8
        # Generate a cancel transaction every X transaction as long as it is not the first
        if i % cancelled_transactions_frequency != 0 or i == 0:
            random_amount = random.randint(1, upper_bound_random_amount)
            mine_blocks_on_ledger(ledger, miners, mining_reward)
            random_user_1.send(random_amount, random_user_2)
        else:
            mine_blocks_on_ledger(ledger, miners, mining_reward)
            random_cancelled_tid = generate_unique_cancelled_tid(
                users, i - 1, ledger.transaction_cancelled_tids)
            ledger.cancel_transaction(random_cancelled_tid)
    return (ledger, users)


def mine_blocks_on_ledger(ledger, miners, mining_reward):
    """ Mine blocks that are full of transactions on the ledger """
    # only mine if the block is full
    try:
        if ledger.is_block_full():
            winning_miner = None
            winning_time = None
            for miner in miners:
                if miner.is_valid_block_chain():
                    start = time.time()
                    miner.last_block_hash()  # race to see who can hash fastest
                    end = time.time()
                    miner_time = end - start
                    if winning_miner == None or miner_time < winning_time:
                        winning_miner = miner
                        winning_time = miner_time
            winning_miner.do_work(mining_reward)  # winner does the mining
    except Exception as e:
        logger.exception('Block is not full')
        raise e


def transaction_generator():
    """
    Generate transactions for the blockchain
    """
    monies, anon, users, miners = create_users_and_ledger()
    initial_balance = 1000
    mining_reward = 10
    # generate the initial balance for all users
    generate_initial_balance(anon, users, initial_balance, mining_reward)
    num_of_generated_trans = 2000
    # generate the remaining transactions minus the initial balances
    return generate_transactions_on_ledger(monies, users, num_of_generated_trans - len(users), miners, mining_reward)
