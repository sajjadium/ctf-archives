from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from shared.gen.messages.v1 import Coords, MapChunk, SessionType


@dataclass
class Position:
    coords: Coords
    time: datetime


@dataclass
class Session:
    type: SessionType = field(default=SessionType.SESSION_TYPE_NORMAL)
    peer: str = field(default_factory=str)
    user_id: str = field(default_factory=str)

    known_objects: set[str] = field(default_factory=set)
    last_positions: list[Position] = field(default_factory=list[Position])
    maze: list[list[MapChunk]] = field(default_factory=list)
    waiting_maze_chunks: list[tuple[int, int]] = field(default_factory=list)

    last_ping: datetime = field(default=datetime.now())
    known_users: set[str] = field(default_factory=set)

    logout: bool = field(default_factory=bool)

    def __getstate__(self) -> None:
        return None

    def __setstate__(self, state: Any) -> None:
        self.__dict__ = Session().__dict__


@dataclass
class ScoreboardEntry:
    user_id: str
    username: str | None = None
    start: datetime | None = None
    end: datetime | None = None

    @property
    def time(self) -> timedelta:
        if self.start and self.end:
            return self.end - self.start

        return timedelta.max

    def reset(self) -> None:
        self.start = None
        self.end = None
