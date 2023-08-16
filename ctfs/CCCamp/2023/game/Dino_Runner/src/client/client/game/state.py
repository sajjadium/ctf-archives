import threading
import time
from datetime import datetime
from types import TracebackType
from typing import Dict, Tuple, cast

import client
from client.game.entities.enemy import Enemy
from client.scenes.game import Game
from shared.constants import TARGET_FPS, TARGET_UPS
from shared.gen.messages.v1 import LoggedIn, Object, SessionType, User


class TimedLock:
    lock: threading.Lock
    t0: float
    t1: float
    frequency: float

    def __init__(self, frequency: float) -> None:
        self.lock = threading.Lock()
        self.frequency = frequency
        self.t0 = 0
        self.t1 = 0

    def __enter__(self) -> bool:
        self.lock.acquire(True)
        self.t0 = time.time()
        return True

    def locked(self) -> bool:
        return self.lock.locked()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.lock.release()
        self.t1 = time.time()


class GameState:
    users: Dict[str, User]
    objects: Dict[str, Tuple[Object, Object]]
    my_user: User | None
    last_ping: datetime
    session_type: SessionType
    draw_lock: TimedLock
    update_lock: TimedLock

    def __init__(self) -> None:
        self.draw_lock = TimedLock(1 / TARGET_FPS)
        self.update_lock = TimedLock(1 / TARGET_UPS)
        self.users = {}
        self.objects = {}
        self.my_user = None
        self.last_ping = datetime.now()
        self.session_type = SessionType.SESSION_TYPE_UNSPECIFIED

    def is_authenticated(self) -> bool:
        return self.my_user is not None

    def login(self, message: LoggedIn) -> None:
        if message.success:
            self.my_user = message.self
            self.session_type = message.type

    def logout(self) -> None:
        self.my_user = None

    def get_objects_in_range(self, distance_squared: float) -> list[Enemy]:
        if self.my_user is None:
            return []

        game_scene = cast(Game, client.scene_manager.current_scene)

        all_enemies = game_scene.enemies.values()

        coords = self.my_user.coords
        return list(
            filter(
                lambda e: ((coords.x - e.x) ** 2) + ((coords.y - e.y) ** 2)
                <= distance_squared,  # TODO: Last or next here?
                all_enemies,
            )
        )
