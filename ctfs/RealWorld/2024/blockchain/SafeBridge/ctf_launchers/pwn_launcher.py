import os

import requests
from eth_abi import abi

from ctf_launchers.launcher import ORCHESTRATOR_HOST, Action, Launcher
from ctf_launchers.team_provider import TeamProvider, get_team_provider
from ctf_launchers.types import UserData, get_privileged_web3

FLAG = os.getenv("FLAG", "rwctf{flag}")


class PwnChallengeLauncher(Launcher):
    def __init__(
        self,
        project_location: str = "challenge/project",
        provider: TeamProvider = get_team_provider(),
    ):
        super().__init__(
            project_location,
            provider,
            [
                Action(name="get flag", handler=self.get_flag),
            ],
        )

    def get_flag(self) -> int:
        instance_body = requests.get(
            f"{ORCHESTRATOR_HOST}/instances/{self.get_instance_id()}"
        ).json()
        if not instance_body["ok"]:
            print(instance_body["message"])
            return 1

        user_data = instance_body["data"]

        if not self.is_solved(user_data, user_data["metadata"]["challenge_address"]):
            print("are you sure you solved it?")
            return 1

        print(FLAG)
        return 0

    def is_solved(self, user_data: UserData, addr: str) -> bool:
        web3 = get_privileged_web3(user_data, "l1")

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
