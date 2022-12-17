from brownie import *

def restricted_accounts():
    return [accounts[9]]

def deploy():
    Jump.deploy({'from': accounts[9], 'value': web3.toWei(1, 'ether')})

def solved():
    if Jump[-1].balance() == 0:
        return True, "Solved!"
    else:
        return False, "Still have funds!"


CONFIG = {
    # "RPC": '',
    # "BLOCK_NUMBER": '',
    # 'FLAGS': '',
    'MNEMONIC': 'test test test test test test test test test test test junk',
    # 'RUNNABLES': [],
    # 'ALLOWED_RPC_METHODS': []
}
