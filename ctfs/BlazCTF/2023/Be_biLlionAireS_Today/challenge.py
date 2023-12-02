from typing import Dict

from ctf_launchers.pwn_launcher import PwnChallengeLauncher
from ctf_server.types import (
    LaunchAnvilInstanceArgs,
    UserData,
    get_privileged_web3,
)

from foundry.anvil import anvil_setBalance

MULTISIG = "0x67CA7Ca75b69711cfd48B44eC3F64E469BaF608C"
ADDITIONAL_OWNER1 = "0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69"
ADDITIONAL_OWNER2 = "0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf"
ADDITIONAL_OWNER3 = "0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF"

class Challenge(PwnChallengeLauncher):
    def deploy(self, user_data: UserData, mnemonic: str) -> str:
        web3 = get_privileged_web3(user_data, "main")
        challenge_addr = super().deploy(user_data, mnemonic)

        anvil_setBalance(web3, MULTISIG, hex(int(10e18)))
        add_owner(web3, ADDITIONAL_OWNER1)
        add_owner(web3, ADDITIONAL_OWNER2)
        add_owner(web3, ADDITIONAL_OWNER3)

        return challenge_addr

    def get_anvil_instances(self) -> Dict[str, LaunchAnvilInstanceArgs]:
        return {
            "main": self.get_anvil_instance(
                balance=1,
                fork_block_num=18_677_777,
            ),
        }

def send_unsigned_transaction(web3, to_addr, from_addr, gas, gas_price, value, data):
    return web3.provider.make_request(
        "eth_sendUnsignedTransaction",
        [
            {
                "to": to_addr,
                "from": from_addr,
                "gas": hex(gas),
                "gasPrice": hex(gas_price),
                "value": value,
                "data": data,
            }
        ],
    )

def add_owner(web3, owner):
    return send_unsigned_transaction(
        web3,
        MULTISIG,
        MULTISIG,
        104941,
        50000000000,
        "0x00",
        # calling addOwnerWithThreshold(address owner = ADDITIONAL_OWNER, uint256 threshold = 3)
        f"0x0d582f13000000000000000000000000{owner.replace('0x', '')}0000000000000000000000000000000000000000000000000000000000000003")


Challenge().run()
