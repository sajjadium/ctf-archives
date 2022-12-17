from brownie import *

def deploy(state, deployer, player):
    Welcome.deploy({'from': deployer[0]})

def solved():
    if Welcome[-1].balance() > 0:
        return True, "Solved!"
    else:
        return False, "Need more coins!"

CONFIG = {
    # "RPC": '',
    # "BLOCK_NUMBER": '',
    # 'FLAGS': '',
    'MNEMONIC': 'test test test test test test test test test test test junk',
    # 'RUNNABLES': [],
    'ALLOWED_RPC_METHODS': []
}
