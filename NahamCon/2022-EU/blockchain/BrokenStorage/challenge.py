from brownie import *


def restricted_accounts():
    return [accounts[8]]

def deploy():
    ADMIN = accounts[8]
    buckets = Buckets.deploy({'from': ADMIN})
    bucketsProxy = BucketsProxy.deploy(buckets, 5, {'from': ADMIN})
    
def solved():    
    ADMIN = accounts[8]
    proxy_buckets = Contract.from_abi("Buckets", BucketsProxy[-1], Buckets.abi)

    if BucketsProxy[-1].getAdmin() != ADMIN and proxy_buckets.balanceOf(ADMIN) == 0x1337:
        return True, "Solved!"
    else:
        return False, "Not solved."

CONFIG = {
    # "RPC": '',
    # "BLOCK_NUMBER": '',
    # 'FLAGS': '',
    'MNEMONIC': 'test test test test test test test test test test test junk',
    # 'RUNNABLES': [],
    # 'ALLOWED_RPC_METHODS': []
}
