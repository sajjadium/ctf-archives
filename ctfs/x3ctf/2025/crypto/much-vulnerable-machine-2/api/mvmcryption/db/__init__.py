from __future__ import annotations

from mvmcryption.environ import getenv

from .db import connect
from .users import Users

ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")

TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
"""


def initialize() -> None:
    with connect() as conn:
        conn.executescript(TABLE_QUERY)
        try:
            Users(conn).create(
                username="admin",
                email="admin@this-company-luckily-does-not-exist.mvm",
                password=ADMIN_PASSWORD,
            )
        except Exception as e:  # maybe it already exists
            print(e)


__all__ = [
    "Users",
    "initialize",
]
