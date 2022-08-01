#!/usr/bin/env python3

import jwt
import typing

import models
import storages


class SessionProvider:
    def __init__(self, users: storages.UserStorage, tokens: storages.TokenStorage):
        self._users = users
        self._tokens = tokens

    async def create(self, credentials: models.Credentials) -> typing.Optional[models.User]:
        obj = {
            'username': credentials.username,
        }

        try:
            session = jwt.encode(obj, credentials.password).decode()
        except Exception:
            return None

        token = self._token(session)
        await self._tokens.insert(token, credentials.username)

        return models.User(
            session=session,
            username=obj['username'],
        )

    async def destroy(self, user: models.User) -> None:
        token = self._token(user.session)
        await self._tokens.delete(token)

    async def validate(self, session: str) -> typing.Optional[models.User]:
        token = self._token(session)
        username = await self._tokens.search(token)

        if username is None:
            return await self.prolongate(session)

        password = await self._users.search(username)

        if password is None:
            return None

        try:
            obj = jwt.decode(session, password)
        except Exception:
            return None

        return models.User(
            session=session, 
            username=obj['username'],
        )

    async def prolongate(self, session: str) -> typing.Optional[models.User]:
        try:
            obj = jwt.decode(session, verify=False)
        except Exception:
            return None

        password = await self._users.search(obj['username'])

        if password is None:
            return None

        try:
            obj = jwt.decode(session, password)
        except Exception:
            return None

        token = self._token(session)
        await self._tokens.insert(token, obj['username'])

        return models.User(
            session=session, 
            username=obj['username'],
        )

    def _token(self, session: str) -> str:
        return session.rsplit('.', 1)[-1]
