from anvil_server.database import UserData
from eth_account.account import LocalAccount
from eth_launchers.pwn_launcher import PwnChallengeLauncher
from eth_launchers.team_provider import get_team_provider
from eth_launchers.utils import anvil_setCodeFromFile


class Challenge(PwnChallengeLauncher):
    def deploy(self, user_data: UserData) -> str:
        anvil_setCodeFromFile(
            user_data.get_privileged_web3("main"),
            "0x7f5C649856F900d15C83741f45AE46f5C6858234",
            "UNCX_ProofOfReservesV2_UniV3.sol:UNCX_ProofOfReservesV2_UniV3",
        )

        return super().deploy(user_data)


Challenge(
    project_location="project",
    provider=get_team_provider(),
).run()
