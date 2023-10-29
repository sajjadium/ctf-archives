from eth_launchers.pwn_launcher import PwnChallengeLauncher
from eth_launchers.team_provider import get_team_provider

PwnChallengeLauncher(
    project_location="project",
    provider=get_team_provider(),
).run()
