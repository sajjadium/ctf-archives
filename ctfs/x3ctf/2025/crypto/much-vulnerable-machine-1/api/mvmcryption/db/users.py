from __future__ import annotations

from argon2 import PasswordHasher, exceptions
from pydantic import EmailStr, SecretStr

from .db import BaseModel, DBModel

PH = PasswordHasher()


class User(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr

    @property
    def is_admin(self):
        return self.id == 1


class Users(DBModel[User]):
    tablename = "users"
    model = User
    columns = (
        "username",
        "email",
        "password",
    )
    mutable_columns = (
        "username",
        "email",
    )

    def find_by_username(self, username: str):
        return self.find_by("username")(username)

    def create(self, *, username: str, email: str, password: str) -> User:
        _password = PH.hash(password)
        return self.insert(
            {"username": username, "email": email, "password": _password},
        )

    def login(self, username: str, password: str) -> User | None:
        if not (u := self.find_by_username(username)):
            return None

        try:
            PH.verify(u.password.get_secret_value(), password)
            return u
        except exceptions.VerifyMismatchError:
            return None
