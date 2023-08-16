import time
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, cast

from pyglet import shapes
from pyglet.window import key

import client
from client.game.entities.enemy import Enemy
from client.game.entities.entity import Direction, InteractEntity, TilesetEntity
from shared.collison import CollisionManager
from shared.constants import PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_WIDTH
from shared.gen.messages.v1 import Activity, SessionType

if TYPE_CHECKING:
    from client.scenes.game import Game

PROGRESSBAR_WIDTH = 40


@dataclass
class Player(TilesetEntity, InteractEntity):
    velocity_x: float
    velocity_y: float
    _direction: Direction

    _x: float = 0.0
    _y: float = 0.0
    _rotation: float = 0.0

    _attacking: bool = False
    _last_attack: float = 0

    def __init__(self, *args: int, **kwargs: str):
        super().__init__(*args, **kwargs)

        self.keys = key.KeyStateHandler()
        self.event_handlers = [self, self.keys]
        self.coords_dirty = False
        self.velocity_x = 0
        self.velocity_y = 0
        self._direction = Direction.DOWN
        self.can_move = True

        self._x = 0
        self._y = 0
        self._rotation = 0

        self._rotation = float(self._direction.value)

        self.speed = PLAYER_SPEED

        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.bb = shapes.Rectangle(
            self.x, self.y, self.width, self.height, color=(255, 0, 30)
        )

        self.collision_manager = CollisionManager(self.width, self.height)

        self.interact_distance = 0
        self._attacking = False
        self._last_attack = 0
        self.progressbar = shapes.BorderedRectangle(
            x=0,
            y=0,
            width=PROGRESSBAR_WIDTH,
            height=7,
            border=3,
            color=(0, 255, 0),
            border_color=(0, 0, 0),
        )
        self.outer_progressbar = shapes.Rectangle(
            x=0, y=0, width=PROGRESSBAR_WIDTH, height=7, color=(179, 174, 173, 127)
        )
        self.progress = -1.0
        self.progressbar_offset_x = 10
        self.progressbar_offset_y = -25

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def rotation(self) -> float:
        return self._rotation

    @direction.setter
    def direction(self, value: Direction) -> None:
        if value != self._direction:
            self.coords_dirty = True
        self._direction = value
        self._rotation = float(value.value)

    @x.setter
    def x(self, value: float) -> None:
        if value != self._x:
            self.coords_dirty = True
        self._x = value

    @y.setter
    def y(self, value: float) -> None:
        if value != self._y:
            self.coords_dirty = True
        self._y = value

    @rotation.setter  # pyright: ignore[reportIncompatibleVariableOverride]
    def rotation(self, value: float) -> None:
        value %= 360
        if value != self._rotation:
            self.coords_dirty = True
        self._rotation = value

    def _find_attack_enemy(self):
        direction = self.rotation_to_directionproto()
        self.sprites[Activity.ACTIVITY_ATTACKING][
            direction
        ].frame_index = 0  # Reset attack animation to start
        self.sprite = self.sprites[Activity.ACTIVITY_ATTACKING][direction]

        objects_in_range: List[Enemy] = client.game_state.get_objects_in_range(
            distance_squared=400
        )

        enemy_obj = None
        # print("Obj in range: " + str(len(objects_in_range)))

        if len(objects_in_range) == 0:
            return

        enemy_obj = objects_in_range[0]  #  TODO: Differentiate between enemies

        client.global_connection.attack_enemy(
            time=datetime.now(), uuid=enemy_obj.uuid, damage=10
        )

    def _update_move(self, dt: float) -> None:
        game: Game = cast("Game", client.scene_manager.current_scene)

        self.velocity_x = 0
        self.velocity_y = 0

        keys = cast(Dict[int, bool], client.scene_manager.keys.data)
        controller = client.scene_manager.controller

        if controller:
            if abs(controller.leftx) >= 0.25:
                self.velocity_x = controller.leftx

            if abs(controller.lefty) >= 0.25:
                self.velocity_y = controller.lefty

        match keys:
            case {key.LEFT: True, key.RIGHT: True} | {key.A: True, key.D: True}:
                pass
            case {key.LEFT: True} | {key.A: True}:
                self.velocity_x = -1
            case {key.RIGHT: True} | {key.D: True}:
                self.velocity_x = 1
            case _:
                pass

        match keys:
            case {key.UP: True, key.DOWN: True} | {key.W: True, key.S: True}:
                pass
            case {key.UP: True} | {key.W: True}:
                self.velocity_y = -1
            case {key.DOWN: True} | {key.S: True}:
                self.velocity_y = 1
            case _:
                pass

        if client.game_state.session_type == SessionType.SESSION_TYPE_NORMAL:
            match keys:
                case {key.SPACE: True}:
                    if self.can_attack():
                        self._attacking = True
                        self._last_attack = time.time()
                        self._find_attack_enemy()

                case _:
                    pass

        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x *= 0.7071  # 1/sqrt(2)
            self.velocity_y *= 0.7071

        self.velocity_x *= self.speed
        self.velocity_y *= self.speed

        new_x = self.x + self.velocity_x * dt
        new_y = self.y + self.velocity_y * dt

        if client.game_state.session_type != SessionType.SESSION_TYPE_FREE_CAM:
            match self.collision_manager.check_collisons(
                game.map,
                self.x,
                self.y,
                new_x,
                new_y,
            ):
                case None:
                    return
                case (next_x, next_y):
                    pass

            if next_x != self.x or next_y != self.y:
                self.activity = Activity.ACTIVITY_WALKING
            else:
                self.activity = Activity.ACTIVITY_IDLE

            # Handle attacking
            # If we attack, we cancel all movements
            if self._attacking:
                self.activity = Activity.ACTIVITY_ATTACKING
                if self.can_attack():  # Attack finished, we might attack again
                    self._attacking = False

            if not self._attacking:
                if next_y > self.y:
                    self.direction = Direction.DOWN
                elif next_y < self.y:
                    self.direction = Direction.UP
                elif next_x > self.x:
                    self.direction = Direction.RIGHT
                elif next_x < self.x:
                    self.direction = Direction.LEFT
                else:
                    if self.velocity_x != 0 and self.velocity_y != 0:
                        pass
                    elif self.velocity_x > 0:
                        self.direction = Direction.RIGHT
                    elif self.velocity_x < 0:
                        self.direction = Direction.LEFT
                    elif self.velocity_y < 0:
                        self.direction = Direction.UP
                    elif self.velocity_y > 0:
                        self.direction = Direction.DOWN

                self.x = next_x  # pyright: ignore[reportIncompatibleVariableOverride]
                self.y = next_y  # pyright: ignore[reportIncompatibleVariableOverride]
        else:
            self.x = new_x  # pyright: ignore[reportIncompatibleVariableOverride]
            self.y = new_y  # pyright: ignore[reportIncompatibleVariableOverride]

    def update(self, dt: float) -> None:
        if self.can_move:
            self._update_move(dt)

        super().update(dt)

    def can_attack(self):
        return time.time() > self._last_attack + 0.600  # One attack is 600ms

    def draw(self) -> None:
        if client.game_state.session_type == SessionType.SESSION_TYPE_FREE_CAM:
            return

        self.bb.x = self.x
        self.bb.y = -self.y

        # Draw health bar below the enemy
        if self.progress >= 0:
            self.outer_progressbar.x = (
                self.x + self.progressbar_offset_x - PROGRESSBAR_WIDTH / 2
            )
            self.outer_progressbar.y = -(self.y + self.progressbar_offset_y)
            self.outer_progressbar.draw()

            self.progressbar.x = (
                self.x + self.progressbar_offset_x - Enemy.HEALTHBAR_WIDTH / 2
            )
            if self.progress > 0 and self.progress <= 1:
                self.progressbar.y = -(self.y + self.progressbar_offset_y)
                self.progressbar.width = int(PROGRESSBAR_WIDTH * (self.progress))
                self.progressbar.draw()
        return super().draw()

    def on_load(self) -> None:
        super().on_load()
