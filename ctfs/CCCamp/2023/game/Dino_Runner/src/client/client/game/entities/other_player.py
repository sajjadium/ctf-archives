from dataclasses import dataclass
from typing import Any

import client
from client.game.entities.entity import (
    Direction,
    NamedEntity,
    ServerManagedEntity,
    TilesetEntity,
)
from shared.gen.messages.v1 import Activity


@dataclass
class OtherPlayer(TilesetEntity, NamedEntity, ServerManagedEntity):
    direction: Direction

    def __init__(self, *args: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.direction = Direction.DOWN

    def update(self, dt: float) -> None:
        if not self.is_loaded:
            return

        new_x = client.game_state.users[self.uuid].coords.x
        new_y = client.game_state.users[self.uuid].coords.y

        rot = client.game_state.users[self.uuid].coords.rotation % 360
        if rot <= 45 or rot >= 315:
            self.direction = Direction.UP
        elif rot >= 135 and rot <= 225:
            self.direction = Direction.DOWN
        elif rot > 45 and rot < 135:
            self.direction = Direction.RIGHT
        elif rot > 135 and rot < 315:
            self.direction = Direction.LEFT
        self.rotation = rot

        if new_x == self.x and new_y == self.y:
            self.activity = Activity.ACTIVITY_IDLE
        else:
            self.activity = Activity.ACTIVITY_WALKING

        self.x = new_x
        self.y = new_y

        super().update(dt)

    def on_load(self) -> None:
        self.label = client.game_state.users[self.uuid].username

        super().on_load()

    def draw(self) -> None:
        return super().draw()
