from anvil_server.database import UserData
from anvil_server.socket import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    GetInstanceRequest,
    UnixClient,
    UpdateMetadataRequest,
)
from eth_abi import abi
from eth_launchers.koth_launcher import KothChallengeLauncher
from eth_launchers.launcher import ETH_RPC_URL
from eth_launchers.score_submitter import ScoreSubmitter, get_score_submitter
from eth_launchers.team_provider import TeamProvider, get_team_provider
from eth_launchers.utils import anvil_setBalance, anvil_setCode
from foundry.anvil import LaunchAnvilInstanceArgs
from web3 import Web3


class Challenge(KothChallengeLauncher):
    def __init__(
        self, project_location: str, provider: TeamProvider, submitter: ScoreSubmitter
    ):
        super().__init__(project_location, provider, submitter, want_metadata=["code"])

    def submit_score(self) -> int:
        client = UnixClient()

        resp = client.get_instance(GetInstanceRequest(id=self.team))
        if not resp.ok:
            print(resp.message)
            return 1

        challenge_addr = resp.user_data.metadata["challenge_address"]

        web3 = resp.user_data.get_privileged_web3("main")

        (code,) = abi.decode(
            ["bytes"],
            web3.eth.call(
                {
                    "to": Web3.to_checksum_address(challenge_addr),
                    "data": Web3.keccak(text="bestImplementation()")[:4].hex(),
                }
            ),
        )

        resp = client.update_metadata(
            UpdateMetadataRequest(
                id=self.team,
                metadata={
                    "code": code.hex(),
                },
            )
        )
        if not resp.ok:
            print(resp.message)
            return 1

        return super().submit_score()


Challenge(
    project_location="project",
    provider=get_team_provider(),
    submitter=get_score_submitter(),
).run()
