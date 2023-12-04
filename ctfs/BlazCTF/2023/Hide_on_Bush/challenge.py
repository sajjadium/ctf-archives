from typing import Dict

from ctf_launchers.pwn_launcher import PwnChallengeLauncher
from ctf_server.types import (
    get_privileged_web3,
    DaemonInstanceArgs,
    LaunchAnvilInstanceArgs,
    UserData,
)

BLOCK_TIME = 12
class Challenge(PwnChallengeLauncher):
    def deploy(self, user_data: UserData, mnemonic: str) -> str:
        web3 = get_privileged_web3(user_data, "main")

        web3.provider.make_request("evm_setAutomine", [True])
        challenge_addr = super().deploy(user_data, mnemonic)
        web3.provider.make_request("evm_setIntervalMining", [BLOCK_TIME])

        return challenge_addr

    def get_anvil_instances(self) -> Dict[str, LaunchAnvilInstanceArgs]:
        return {
            "main": self.get_anvil_instance(
                fork_url=None,
                accounts=3,
                block_time=BLOCK_TIME,
            ),
        }

    def get_daemon_instances(self) -> Dict[str, DaemonInstanceArgs]:
        return {
            "daemon": DaemonInstanceArgs(
                image="fuzzland/hide-on-bush-daemon:latest"
            )
        }

Challenge().run()
