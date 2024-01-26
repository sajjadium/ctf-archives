import abc
import os
from hashlib import md5
from typing import Optional

import requests


class TeamProvider(abc.ABC):
    @abc.abstractmethod
    def get_team(self) -> Optional[str]:
        pass


class LocalTeamProvider(TeamProvider):
    def __init__(self, team_id):
        self.__team_id = team_id

    def get_team(self):
        return self.__team_id


class RemoteTeamProvider(TeamProvider):
    def __init__(self, rw_api_token):
        self.__rw_api_token = rw_api_token

    def get_team(self):
        team_id = self.__check(input("team token? "))
        if not team_id:
            print("invalid team token!")
            return None

        return team_id

    def __check(self, token: str) -> str:
        response = requests.get(
            "https://realworldctf.com/api/team/info",
            headers={"token": self.__rw_api_token},
            timeout=8,
        )
        json = response.json()
        assert json["msg"] == "success"
        try:
            for team in json["data"]:
                if team["hash"] == md5(token.encode()).hexdigest():
                    return team["hash"]
        except Exception as e:
            print(e)

        return None


def get_team_provider() -> TeamProvider:
    rw_api_token = os.getenv("API_TOKEN")
    if rw_api_token:
        return RemoteTeamProvider(rw_api_token)
    else:
        return LocalTeamProvider(team_id="local")
