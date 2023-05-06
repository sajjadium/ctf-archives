#!/usr/bin/env python3

import json
import typing
import aioredis


class AbstractStorage:
    PREFIX: str = 'prefix'
    EXPIRATION: int = 0  # seconds

    def __init__(self, storage: aioredis.Redis):
        self._storage = storage

    async def search(self, key: str) -> typing.Optional[object]:
        result = await self._storage.get(self._key(key))

        if result is None:
            return None

        try:
            return json.loads(result)
        except Exception:
            return None

    async def insert(self, key: str, value: object) -> bool:
        obj = json.dumps(value)

        return await self._storage.set(
            self._key(key), obj, self.EXPIRATION,
        )

    async def persist(self, key: str) -> None:
        await self._storage.persist(self._key(key))

    async def delete(self, key: str) -> None:
        await self._storage.delete(self._key(key))

    def _key(self, key: str) -> str:
        return f'{self.PREFIX}_{key}'


class UserStorage(AbstractStorage):
    PREFIX = 'users'
    EXPIRATION = 30 * 60  # 30 minutes


class NoteStorage(AbstractStorage):
    PREFIX = 'notes'
    EXPIRATION = 30 * 60  # 30 minutes


class TokenStorage(AbstractStorage):
    PREFIX = 'tokens'
    EXPIRATION = 5 * 60  # 5 minutes
