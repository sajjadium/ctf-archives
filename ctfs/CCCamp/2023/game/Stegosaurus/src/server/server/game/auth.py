import json
from pathlib import Path

from shared.gen.messages.v1 import SessionType

auth_path: str


def auth(username: str, password: str) -> SessionType | None:
    with open(Path(auth_path), "r") as f:
        users = json.load(f)

    for u, p in users["users"].items():
        if username[:-1] == u and username[-1].isnumeric():
            if p == password:
                return SessionType.SESSION_TYPE_NORMAL

    for u, p in users["freecam"].items():
        if username[:-1] == u and username[-1].isnumeric():
            if p == password:
                return SessionType.SESSION_TYPE_FREE_CAM

    return None
