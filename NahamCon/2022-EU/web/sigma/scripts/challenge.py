from brownie import *

def deploy():
    pass
    # EscrowReward.at('0x34a1Ba8Ab01a78747e3623be9Fa90926e0019c87')

    # transferOp1 = (
    #     0,
    #     ADMIN,
    #     approve_selector,
    #     HALF_ETHER,
    #     approve_signature["signature"]
    # )

    # transferOp2 = (
    #     0,
    #     EscrowReward[0].address,
    #     transferFrom_selector,
    #     HALF_ETHER,
    #     transfer_signature["signature"]
    # )

    # EscrowReward[0].execute(transferOp1, approve_hash)
    # EscrowReward[0].execute(transferOp2, transfer_hash)

def solved():
    rewardNFT = RewardNFT.at(EscrowReward[0].rewardNFT())
    if rewardNFT.totalSupply() > 0:
        return True, "You are a true white hat!"
    else:
        return False, "You still need to mint 1 Reward NFT and safe the world"


CONFIG = {
    # 'RPC': '',
    # 'BLOCK_NUMBER': '',
    # 'FLAGS': '',
    'MNEMONIC': 'test test test test test test test test test test test junk',
    # 'RUNNABLES': [],
    # 'ALLOWED_RPC_METHODS': []
}
