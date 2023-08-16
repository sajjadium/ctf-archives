import time
from dataclasses import dataclass
from typing import Any

from pyglet import shapes

import client
from client.game.entities.entity import (
    InteractEntity,
    NamedEntity,
    ServerManagedEntity,
    TilesetEntity,
)
from shared.constants import SERVER_TICK_RATE
from shared.gen.messages.v1 import Activity, InteractStatus


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
class Enemy(TilesetEntity, NamedEntity, InteractEntity, ServerManagedEntity):
    HEALTHBAR_WIDTH = 40
    health: int
    health_max: int
    last_attack: float
    is_dead: bool
    dead_time: float

    def __init__(
        self,
        health: int,
        health_max: int,
        last_attack: float,
        *args: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.rotation = 90.0
        self.activity = Activity.ACTIVITY_IDLE

        self.label = "T-RRRRRRREX"

        self.bb = None
        self.bb_offset_x = 4
        self.bb_offset_y = -3

        self.last_x = 0
        self.next_x = 0
        self.last_y = 0
        self.next_y = 0

        self.in_interaction = False
        self.interact_distance = 0

        self.health = health
        self.health_max = health_max

        self.health_bar = None
        self.health_bar_outer = None

        self.health_bar_offset_x = 10
        self.health_bar_offset_y = -25

        self.is_dead = False
        self.dead_time = 0
        self.last_attack = last_attack

    def on_load(self) -> None:
        self.bb = shapes.Rectangle(
            self.x + self.bb_offset_x,
            -(self.y + self.bb_offset_y),
            self.width,
            self.height,
            color=(0, 0, 255),
        )

        # TEMP: Draw circle for aggro notice
        self.bb = shapes.Circle(
            x=self.x,
            y=-(self.y),
            radius=80,
            color=(0, 0, 255, 40),
        )

        self.health_bar = shapes.BorderedRectangle(
            x=0,
            y=0,
            width=Enemy.HEALTHBAR_WIDTH,
            height=7,
            border=3,
            color=(255, 0, 0),
            border_color=(0, 0, 0),
        )
        self.health_bar_outer = shapes.Rectangle(
            x=0, y=0, width=Enemy.HEALTHBAR_WIDTH, height=7, color=(179, 174, 173, 127)
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

        # Update other properties like health, name, ...
        self.health = client.game_state.objects[self.uuid][1].enemy_info.health
        self.health_max = client.game_state.objects[self.uuid][1].enemy_info.health_max
        self.name = client.game_state.objects[self.uuid][1].enemy_info.name
        self.last_attack = client.game_state.objects[self.uuid][
            1
        ].enemy_info.last_attack

        self.label = (
            f"{self.name} ({self.health} HP)"  # TODO: make name label update better
        )

        if time.time() - self.last_attack < 1:  # Attack was in last second
            self.activity = Activity.ACTIVITY_ATTACKING

        if self.health <= 0 and self.is_dead == False:
            self.is_dead = True
            self.dead_time = time.time()
        elif self.health > 0:
            self.is_dead = False

        if self.is_dead:
            self.activity = Activity.ACTIVITY_DEATH
            self.label = ""

        if self.x > new_x:
            self.rotation = 270
        else:
            self.rotation = 90

        self.x = new_x
        self.y = new_y

        super().update(dt)

    def draw(self) -> None:
        if self.is_dead and (time.time() - self.dead_time) > 0.5:
            return  # Dont draw enemey after death animation

        if self.bb is not None:
            self.bb.x = self.x + self.bb_offset_x
            self.bb.y = -(self.y + self.bb_offset_y)
            self.bb.draw()

        if self.health > 0:
            # Draw health bar below the enemy
            if self.health_bar_outer is not None:
                self.health_bar_outer.x = (
                    self.x + self.health_bar_offset_x - Enemy.HEALTHBAR_WIDTH / 2
                )
                self.health_bar_outer.y = -(self.y + self.health_bar_offset_y)
                self.health_bar_outer.draw()

            if self.health_bar is not None and self.health_max != 0:
                self.health_bar.x = (
                    self.x + self.health_bar_offset_x - Enemy.HEALTHBAR_WIDTH / 2
                )
                self.health_bar.y = -(self.y + self.health_bar_offset_y)
                self.health_bar.width = int(
                    Enemy.HEALTHBAR_WIDTH * (self.health / self.health_max)
                )
                self.health_bar.draw()

        return super().draw()
