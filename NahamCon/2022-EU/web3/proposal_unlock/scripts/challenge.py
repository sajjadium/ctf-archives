from brownie import *

def deploy(state, deployer, player):

    ADMIN = deployer[0] 

    vedeg = VeHAL.deploy(web3.toWei(100, 'ether'), "Voting HAL", 18, "VeHAL", {'from':ADMIN})
    deg = HAL.deploy(web3.toWei(1000000, 'ether'), "HAL Token", 18, "HAL", {'from':ADMIN})
    on = OnboardProposal.deploy(deg, vedeg, {'from':ADMIN})

    t1 = Token.deploy("Token1", "T1", {'from':ADMIN})
    on.propose("Token name", t1, 100, 100, {'from':ADMIN})

    # Vote to already pass the proposal, as admin has enough power
    # claiming the airdrop will not allow the proposal to pass, as 30%
    # of total supply is required
    on.vote(1, 1, web3.toWei(100, 'ether') * 0.3, {'from':ADMIN})

def solved(state, deployer, player):
    on = OnboardProposal[-1]
    # Check if any proposal from id 2 up is passed
    for i in range(2, on.proposalCounter() + 1):
        # Check if passed
        if on.proposals(i)[-1] == 1:
            return True, "Solved!"
    return False, "No proposal was passed"


CONFIG = {
    # "RPC": '',
    # "BLOCK_NUMBER": '',
    # 'FLAGS': '',
    'MNEMONIC': 'test test test test test test test test test test test junk',
    # 'RUNNABLES': [],
    'ALLOWED_RPC_METHODS': ["evm_increaseTime", "evm_mine"]
}
