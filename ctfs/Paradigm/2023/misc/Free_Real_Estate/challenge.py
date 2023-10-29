import json
from typing import List

from anvil_server.database import UserData
from anvil_server.socket import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    UnixClient,
)
from eth_launchers.koth_launcher import KothChallengeLauncher
from eth_launchers.launcher import ETH_RPC_URL
from eth_launchers.score_submitter import ScoreSubmitter, get_score_submitter
from eth_launchers.team_provider import TeamProvider, get_team_provider
from eth_launchers.utils import deploy
from foundry.anvil import LaunchAnvilInstanceArgs


class Challenge(KothChallengeLauncher):
    def __init__(
        self, project_location: str, provider: TeamProvider, submitter: ScoreSubmitter
    ):
        super().__init__(
            project_location, provider, submitter, want_metadata=["claimed"]
        )

    def create_instance(self, client: UnixClient) -> CreateInstanceResponse:
        return client.create_instance(
            CreateInstanceRequest(
                id=self.team,
                instances={
                    "main": LaunchAnvilInstanceArgs(
                        balance=1000,
                        fork_url=ETH_RPC_URL,
                    ),
                },
                daemons=[
                    "/home/user/watcher.py",
                ],
            )
        )

    def deploy(self, user_data: UserData) -> str:
        with open("airdrop-merkle-proofs.json", "r") as f:
            airdrop_data = json.load(f)

        web3 = user_data.get_privileged_web3("main")

        return deploy(
            web3,
            self.project_location,
            user_data.mnemonic,
            env={
                "MERKLE_ROOT": airdrop_data["merkleRoot"],
                "TOKEN_TOTAL": airdrop_data["tokenTotal"],
            },
        )


Challenge(
    project_location="project",
    provider=get_team_provider(),
    submitter=get_score_submitter(),
).run()
