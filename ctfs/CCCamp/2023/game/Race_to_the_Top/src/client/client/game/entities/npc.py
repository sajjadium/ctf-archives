from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

from pyglet import shapes

import client
from client.game.entities.entity import (
    Direction,
    InteractEntity,
    NamedEntity,
    ServerManagedEntity,
    TilesetEntity,
)
from shared.constants import SERVER_TICK_RATE
from shared.gen.messages.v1 import Activity, InteractStatus

if TYPE_CHECKING:
    from client.scenes.game import Game


def is_c_between_ab(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    epsilon: float = 4,  # this is in pixels, so this can be quite large
) -> tuple[bool, float]:
    # check aabb
    minX, maxX = (a[0], b[0]) if a[0] < b[0] else (b[0], a[0])
    minY, maxY = (a[1], b[1]) if a[1] < b[1] else (b[1], a[1])

    if (
        c[0] < (minX - epsilon)
        or c[0] > (maxX + epsilon)
        or c[1] < (minY - epsilon)
        or c[1] > (maxY + epsilon)
    ):
        return False, -1
    if b[1] != a[1] and c[1] != a[1]:
        s1 = (b[0] - a[0]) / (b[1] - a[1])
        s2 = (c[0] - a[0]) / (c[1] - a[1])
        return abs(s1 - s2) < epsilon, abs(s1 - s2)
    if b[0] != a[0] and c[0] != a[0]:
        s1 = (b[1] - a[1]) / (b[0] - a[0])
        s2 = (c[1] - a[1]) / (c[0] - a[0])
        return abs(s1 - s2) < epsilon, abs(s1 - s2)
    return True, -1


@dataclass
class NPC(TilesetEntity, NamedEntity, InteractEntity, ServerManagedEntity):
    def __init__(self, *args: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.rotation = 270.0
        self.activity = Activity.ACTIVITY_IDLE

        self.label = "UNKNOWN"

        self.bb = None
        self.bb_offset_x = 4
        self.bb_offset_y = -3

        self.last_x = 0
        self.next_x = 0
        self.last_y = 0
        self.next_y = 0

        self.in_interaction = False
        self.interact_distance = 0

    def on_load(self) -> None:
        self.bb = shapes.Rectangle(
            self.x + self.bb_offset_x,
            -(self.y + self.bb_offset_y),
            self.width,
            self.height,
            color=(0, 0, 255),
        )

        super().on_load()

    def stop_interaction(self) -> None:
        if self.in_interaction:
            if self.sprite:
                self.sprite.scale_x = 1

            client.global_connection.interact(
                self.uuid, text="", status=InteractStatus.INTERACT_STATUS_STOP
            )

        super().stop_interaction()

    def interact(self, input: str = "") -> None:
        game = cast("Game", client.scene_manager.current_scene)
        player = game.player

        px = player.x + player.interact_offset[0]
        py = player.y + player.interact_offset[1]

        sx = self.x + self.interact_offset[0]
        sy = self.y + self.interact_offset[1]
        # make dino look at player
        if px < sx:
            if self.sprite:
                self.sprite.scale_x = -1

        # make player look at dino

        dx = px - sx
        dy = py - sy

        if abs(dx) > abs(dy):
            if dx < 0:
                player.direction = Direction.RIGHT
            else:
                player.direction = Direction.LEFT
        else:
            if dy < 0:
                player.direction = Direction.DOWN
            else:
                player.direction = Direction.UP
                pass

        if self.in_interaction:
            client.global_connection.interact(
                self.uuid, text=input, status=InteractStatus.INTERACT_STATUS_UPDATE
            )
        else:
            client.global_connection.interact(
                self.uuid, text=input, status=InteractStatus.INTERACT_STATUS_START
            )

        super().interact()

    def update(self, dt: float) -> None:
        next_x = client.game_state.objects[self.uuid][1].coords.x
        next_y = client.game_state.objects[self.uuid][1].coords.y
        last_x = client.game_state.objects[self.uuid][0].coords.x
        last_y = client.game_state.objects[self.uuid][0].coords.y

        if next_x != last_x or next_y != last_y:
            self.activity = Activity.ACTIVITY_WALKING

        pred_x = self.x + (next_x - last_x) * (SERVER_TICK_RATE * dt)
        pred_y = self.y + (next_y - last_y) * (SERVER_TICK_RATE * dt)
        val, _err = is_c_between_ab(
            (last_x, last_y), (next_x, next_y), (pred_x, pred_y)
        )

        if val:
            # pred okay
            new_x = pred_x
            new_y = pred_y
        else:
            # miss
            new_x = last_x
            new_y = last_y

        if self.x > new_x:
            self.rotation = 270
        else:
            self.rotation = 90

        self.x = new_x
        self.y = new_y

        super().update(dt)

    def draw(self) -> None:
        if self.bb is not None:
            self.bb.x = self.x + self.bb_offset_x
            self.bb.y = -(self.y + self.bb_offset_y)
            self.bb.draw()

        return super().draw()
