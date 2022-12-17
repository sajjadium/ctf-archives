from brownie import *
from brownie import convert


def restricted_accounts():
    return [accounts[9]]

def deploy():
    ADMIN = accounts[9]
    token = SimpleToken.deploy('Simple Token', 'STK', {'from': ADMIN})
    _merkleRoot = 0x654ef3fa251b95a8730ce8e43f44d6a32c8f045371ce6a18792ca64f1e148f8c
    airdrop = Airdrop.deploy(token, 1e5, _merkleRoot, 4, {'from': ADMIN})
    token.setAirdropAddress(airdrop, {'from': ADMIN})

    merkleProof = [
        int(convert.to_bytes(ADMIN.address).hex(),16),
        0x000000000000000000000000feb7377168914e8771f320d573a94f80ef953782,
        0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6,
        0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563
    ]

    airdrop.mintToken(merkleProof)

def solved():
    token = SimpleToken[-1]

    # You should mint 100000 amount of token.
    if token.totalSupply() == 200000:
        return True, "Solved!"
    else:
        return False, "Not solved, you need to mint enough to solve."


CONFIG = {
    # "RPC": '',
    # "BLOCK_NUMBER": '',
    # 'FLAGS': '',
    'MNEMONIC': 'test test test test test test test test test test test junk',
    # 'RUNNABLES': [],
    # 'ALLOWED_RPC_METHODS': []
}
