import os
from typing import Optional

from anvil_server.database import UserData
from eth_launchers.pwn_launcher import PwnChallengeLauncher
from eth_launchers.team_provider import get_team_provider
from eth_launchers.utils import deploy


def concat_env(a: Optional[str], b: Optional[str]):
    if not a and not b:
        return ""
    if not a:
        return b
    if not b:
        return a

    return a + os.pathsep + b


class Challenge(PwnChallengeLauncher):
    def deploy(self, user_data: UserData) -> str:
        web3 = user_data.get_privileged_web3("main")

        return deploy(
            web3,
            self.project_location,
            user_data.mnemonic,
            env={
                "PATH": concat_env("/opt/huff/bin:/usr/bin", os.getenv("PATH")),
            },
        )


Challenge(
    project_location="project",
    provider=get_team_provider(),
).run()
