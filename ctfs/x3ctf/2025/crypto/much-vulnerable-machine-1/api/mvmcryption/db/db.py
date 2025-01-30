from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from typing import Annotated, Generic, TypeVar

from fastapi import Depends
from pydantic import BaseModel as _BaseModel

from mvmcryption.environ import getenv

DB_PATH = getenv("DB_PATH")


def connect_dependency() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.autocommit = True
    return conn


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    conn = connect_dependency()
    try:
        yield conn
    finally:
        conn.close()


class BaseModel(_BaseModel):
    id: int


T = TypeVar("T", bound=BaseModel)
V = TypeVar("V")


class DBModel(ABC, Generic[T]):
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    @classmethod
    @property
    @abstractmethod
    def tablename(cls) -> str:
        raise NotImplementedError

    @classmethod
    @property
    @abstractmethod
    def columns(cls) -> Sequence[str]:
        raise NotImplementedError

    @classmethod
    @property
    @abstractmethod
    def mutable_columns(cls) -> Sequence[str]:
        raise NotImplementedError

    @classmethod
    @property
    @abstractmethod
    def model(cls) -> type[T]:
        raise NotImplementedError

    @classmethod
    @property
    def select_query(cls) -> str:
        return f"SELECT * FROM {cls.tablename} "

    @classmethod
    @property
    def delete_query(cls) -> str:
        return f"DELETE FROM {cls.tablename} "

    @classmethod
    @property
    def insert_query(cls) -> str:
        return f"INSERT INTO {cls.tablename} ({', '.join(cls.columns)}) VALUES ({', '.join(f':{col}' for col in cls.columns)}) RETURNING *;"

    @classmethod
    @property
    def update_query(cls) -> str:
        return f"UPDATE {cls.tablename} SET {', '.join([f'{col} = :{col}' for col in cls.mutable_columns])} "

    @contextmanager
    def cur(self) -> Iterator[sqlite3.Cursor]:
        cur = self.conn.cursor()
        try:
            yield cur
        finally:
            cur.close()

    def delete(self, id: int) -> None:
        return self.delete_by("id")(id)

    def delete_by(self, lookup: str) -> None:
        q = self.delete_query + f"WHERE {lookup} = ?;"

        def _delete_by(value) -> None:
            with self.cur() as cur:
                cur.execute(q, [value])

        return _delete_by

    def insert(self, params: dict, **kwargs) -> T:
        with self.cur() as cur:
            cur.execute(self.insert_query, params, **kwargs)
            record = cur.fetchone()
            return self.model(**record)

    def update(self, id: int, params: dict) -> T:
        return self.update_by("id")(id, params)

    def update_by(self, lookup: str) -> Callable[[dict, ...], T]:
        if not self.update_query:
            raise Exception("Model is readonly.")

        q = self.update_query + f"WHERE {lookup} = :lookup RETURNING *;"

        def _update_by(value, params: dict, **kwargs) -> T:
            params["lookup"] = value

            with self.cur() as cur:
                cur.execute(q, params, **kwargs)
                record = cur.fetchone()
                return self.model(**record)

        return _update_by

    def find(self, id: int) -> T | None:
        return self.find_by("id")(id)

    def find_by(self, lookup: str) -> Callable[[V], T]:
        q = self.select_query + f"WHERE {lookup} = :{lookup};"

        def _find_by(value) -> T | None:
            with self.cur() as cur:
                cur.execute(q, [value])
                if record := cur.fetchone():
                    return self.model(**record)
                return None

        return _find_by

    def all(self) -> list[T]:
        q = self.select_query + ";"
        with self.cur() as cur:
            cur.execute(q)
            return [self.model(**record) for record in cur.fetchall()]

    @classmethod
    def dependency(cls, db: Annotated[sqlite3.Connection, Depends(connect_dependency)]):
        return cls(db)
