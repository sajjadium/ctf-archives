from brownie import *

def deploy(state, deployer, player):

    ADMIN = deployer[0]

    l = LdcNFT.deploy('LdcNFT', 'LDC', 'http://halborn.com', {'from':ADMIN})

    l.flipPublicSaleOn({'from': ADMIN})
    l.flipSantaAlgorithmOn({'from': ADMIN})

    ADMIN.transfer(l, web3.toWei(6, 'ether'))


def solved(state, deployer, player):

    l = LdcNFT[-1]

    # You should have claimed 6 times the prize1ETH prize
    if l.totalSupply() == 6 and l.balance() < web3.toWei(0.5, 'ether'):
        return True, "Solved!"
    else:
        return False, "Not solved, still have {:.2f} ETH in prize".format(web3.fromWei(l.prizeAmount(), 'ether'))


CONFIG = {
    # "RPC": '',
    # "BLOCK_NUMBER": '',
    # 'FLAGS': '',
    'MNEMONIC': 'test test test test test test test test test test test junk',
    # 'RUNNABLES': [],
    'ALLOWED_RPC_METHODS': ["evm_mine", "evm_increaseTime"]
}
