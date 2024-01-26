from typing import Dict

from eth_abi import abi

from ctf_launchers.pwn_launcher import PwnChallengeLauncher
from ctf_launchers.types import (DaemonInstanceArgs, LaunchAnvilInstanceArgs,
                                 UserData, get_additional_account,
                                 get_privileged_web3)
from ctf_launchers.utils import (anvil_setCodeFromFile, anvil_setStorageAt,
                                 deploy)


class Challenge(PwnChallengeLauncher):
    def get_anvil_instances(self) -> Dict[str, LaunchAnvilInstanceArgs]:
        return {
            "l1": self.get_anvil_instance(chain_id=78704, accounts=3, fork_url=None),
            "l2": self.get_anvil_instance(chain_id=78705, accounts=3, fork_url=None),
        }

    def get_daemon_instances(self) -> Dict[str, DaemonInstanceArgs]:
        return {"relayer": DaemonInstanceArgs(image="safe-bridge-relayer:latest")}

    def deploy(self, user_data: UserData, mnemonic: str) -> str:
        l1_web3 = get_privileged_web3(user_data, "l1")
        l2_web3 = get_privileged_web3(user_data, "l2")

        challenge = deploy(
            l1_web3,
            self.project_location,
            mnemonic=mnemonic,
            env={
                "L1_RPC": l1_web3.provider.endpoint_uri,
                "L2_RPC": l2_web3.provider.endpoint_uri,
            },
        )

        anvil_setCodeFromFile(
            l2_web3,
            "0x420000000000000000000000000000000000CAFe",
            "L2CrossDomainMessenger.sol:L2CrossDomainMessenger",
        )
        relayer = get_additional_account(mnemonic, 0)
        anvil_setStorageAt(
            l2_web3,
            "0x420000000000000000000000000000000000CAFe",
            hex(0),
            "0x" + relayer.address[2:].rjust(64, "0"),
        )
        default_xdomain_sender = "0x000000000000000000000000000000000000dEaD"
        anvil_setStorageAt(
            l2_web3,
            "0x420000000000000000000000000000000000CAFe",
            hex(5),
            "0x" + default_xdomain_sender[2:].rjust(64, "0"),
        )

        anvil_setCodeFromFile(
            l2_web3,
            "0x420000000000000000000000000000000000baBe",
            "L2ERC20Bridge.sol:L2ERC20Bridge",
        )
        l2messenger_addr = "0x420000000000000000000000000000000000CAFe"
        (l1_bridge_addr,) = abi.decode(
            ["address"],
            l1_web3.eth.call(
                {
                    "to": challenge,
                    "data": l1_web3.keccak(text="BRIDGE()")[:4].hex(),
                }
            ),
        )
        anvil_setStorageAt(
            l2_web3,
            "0x420000000000000000000000000000000000baBe",
            hex(0),
            "0x" + l2messenger_addr[2:].rjust(64, "0"),
        )
        anvil_setStorageAt(
            l2_web3,
            "0x420000000000000000000000000000000000baBe",
            hex(1),
            "0x" + l1_bridge_addr[2:].rjust(64, "0"),
        )

        anvil_setCodeFromFile(
            l2_web3,
            "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000",
            "L2WETH.sol:L2WETH",
        )

        return challenge


Challenge().run()
