from anvil_server.database import UserData
from anvil_server.socket import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    UnixClient,
)
from eth_abi import abi
from eth_launchers.launcher import ETH_RPC_URL
from eth_launchers.pwn_launcher import PwnChallengeLauncher
from eth_launchers.team_provider import get_team_provider
from eth_launchers.utils import (
    anvil_autoImpersonateAccount,
    anvil_setCodeFromFile,
    anvil_setStorageAt,
    deploy,
)
from foundry.anvil import LaunchAnvilInstanceArgs


class Challenge(PwnChallengeLauncher):
    def create_instance(self, client: UnixClient) -> CreateInstanceResponse:
        return client.create_instance(
            CreateInstanceRequest(
                id=self.team,
                instances={
                    "l1": LaunchAnvilInstanceArgs(
                        balance=1000,
                        chain_id=78704,
                    ),
                    "l2": LaunchAnvilInstanceArgs(
                        path="/opt/foundry/bin/anvil-l2",
                        balance=1000,
                        chain_id=78705,
                    ),
                },
                daemons=[
                    "/home/user/relayer.py",
                ],
            )
        )

    def deploy(self, user_data: UserData) -> str:
        l1_web3 = user_data.get_privileged_web3("l1")
        l2_web3 = user_data.get_privileged_web3("l2")

        anvil_autoImpersonateAccount(l2_web3, True)
        challenge = deploy(
            l1_web3,
            self.project_location,
            mnemonic=user_data.mnemonic,
            env={
                "L1_RPC": l1_web3.provider.endpoint_uri,
                "L2_RPC": l2_web3.provider.endpoint_uri,
            },
        )
        anvil_autoImpersonateAccount(l2_web3, False)

        # deploy multisig
        anvil_setCodeFromFile(
            l2_web3,
            "0x0000000000000000000000000000000000031337",
            "MultiSig.sol:SimpleMultiSigGov",
        )
        for i in range(3):
            owner_addr = user_data.get_additional_account(1 + i)
            anvil_setStorageAt(
                l2_web3,
                "0x0000000000000000000000000000000000031337",
                hex(i),
                "0x" + owner_addr.address[2:].ljust(64, "0"),
            )

        return challenge

    def is_solved(self, user_data: UserData, addr: str) -> bool:
        web3 = user_data.get_privileged_web3("l1")

        (result,) = abi.decode(
            ["bool"],
            web3.eth.call(
                {
                    "to": addr,
                    "data": web3.keccak(text="isSolved()")[:4],
                }
            ),
        )
        return result


Challenge(
    project_location="project",
    provider=get_team_provider(),
).run()
