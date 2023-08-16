import math
import sys
import time
from dataclasses import dataclass
from typing import Any, cast

import server
from server.game.entity.npc import NPCPath
from server.game.entity.object import Object
from server.game.entity.statemachine import STATE_CONTINUE, BaseState, StateMachine
from server.game.secret import ITEMS
from shared.gen.messages.v1 import EnemyInfo, EntityAssets
from shared.gen.messages.v1 import Object as ObjectProto
from shared.gen.messages.v1 import ObjectType, Polygon, SessionType, User

STATE_ALIVE = 0
STATE_DEAD = 1


@dataclass(kw_only=True)
class Enemy(Object):
    health: int
    speed: float
    last_attack: float

    # UUID of the user this enemy object belongs to
    user_uuid: str | None

    state_machine: StateMachine

    def __init__(
        self,
        entity_assets: EntityAssets,
        health: int = 10,
        health_max: int = 100,
        user_uuid: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.health = health
        self.health_max = health_max

        self.user_uuid = user_uuid
        self.entity_assets = entity_assets
        super().__init__(*args, **kwargs)

        self.type = ObjectType.OBJECT_TYPE_ENEMY
        self.state_machine = StateMachine()
        self.last_attack = 0

    async def update(self, dt: float) -> None:
        await super().update(dt=dt)

        await self.state_machine.update(dt)

        # TODO: update if dead?
        # TODO: Pathing, state machine for attacking
        if self.user_uuid is not None:
            await server.global_server.move_enemy_object(
                uuid=self.uuid,
                health=self.health,
                health_max=self.health_max,
                last_attack=self.last_attack,
                name=self.name,
                x=self.x,
                y=self.y,
                include_user_ids=[self.user_uuid],
            )

    async def take_damage(self, damage: int) -> None:
        self.health -= damage

    def is_alive(self):
        return self.health > 0

    def get_distance_to_player(self, user: User) -> float:
        if (
            user.uuid not in server.game_state.user_sessions
            or server.game_state.user_sessions[user.uuid].type
            == SessionType.SESSION_TYPE_FREE_CAM
        ):
            return sys.float_info.max

        player_asset = server.game_state.map.player_asset

        dx = (user.coords.x + player_asset.width / 2) - (
            (self.x + self.entity_assets.width / 2)
        )
        dy = (user.coords.y - player_asset.height / 2) - (
            (self.y - self.entity_assets.height / 2)
        )

        dist_sqrt = math.sqrt(dx**2 + dy**2)
        return dist_sqrt

    def to_proto(self) -> ObjectProto:
        o = super().to_proto()

        o.enemy_info = EnemyInfo(
            health=self.health,
            health_max=self.health_max,
            last_attack=self.last_attack,
            name=self.name,
        )

        return o


class PatrolState(BaseState):
    AGGRO_RADIUS = 80

    def __init__(self, param: object):
        super().__init__(name="patrol", param=param)

    async def update(self, dt: float) -> str:
        self_obj = cast(PatrolEnemy, self.parameter)

        x, y = self_obj.patrol_path.get_next_position(dt, self_obj.x, self_obj.y)
        self_obj.x = x
        self_obj.y = y

        if (
            not self_obj.user_uuid is None
            and self_obj.user_uuid in server.game_state.users
        ):
            clostest_player = server.game_state.users[self_obj.user_uuid]
            dist = self_obj.get_distance_to_player(clostest_player)

            if dist < PatrolState.AGGRO_RADIUS:
                return "aggro"

        return STATE_CONTINUE


class AggroState(BaseState):
    DEAGGRO_RADIUS = 80

    def __init__(self, param: object):
        super().__init__(name="aggro", param=param)

    async def update(self, dt: float) -> str:
        self_obj = cast(PatrolEnemy, self.parameter)
        assert self_obj.user_uuid

        if self_obj.user_uuid not in server.game_state.users:
            return STATE_CONTINUE

        clostest_player = server.game_state.users[self_obj.user_uuid]
        dist = self_obj.get_distance_to_player(clostest_player)

        if dist > AggroState.DEAGGRO_RADIUS:
            return "patrol"

        if dist < AttackingState.ATTACK_RADIUS:
            return "attacking"

        direction_x = clostest_player.coords.x - self_obj.x
        direction_y = clostest_player.coords.y - self_obj.y

        direction_len = math.sqrt(direction_x**2 + direction_y**2)

        direction_x_norm = direction_x / direction_len
        direction_y_norm = direction_y / direction_len

        self_obj.x += direction_x_norm * self_obj.speed * dt
        self_obj.y += direction_y_norm * self_obj.speed * dt

        return STATE_CONTINUE


class AttackingState(BaseState):
    ATTACK_RADIUS = 20
    ATTACK_SPEED = 3

    def __init__(self, param: object):
        super().__init__(name="attacking", param=param)
        self.last_attack = 0

    async def update(self, dt: float) -> str:
        self_obj = cast(PatrolEnemy, self.parameter)
        assert self_obj.user_uuid is not None

        if self_obj.user_uuid not in server.game_state.users:
            return STATE_CONTINUE

        clostest_player = server.game_state.users[self_obj.user_uuid]
        dist = self_obj.get_distance_to_player(clostest_player)

        if dist > AttackingState.ATTACK_RADIUS:
            return "aggro"

        if time.time() > self.last_attack + AttackingState.ATTACK_SPEED:
            await server.global_server.give_damage(
                self_obj.uuid, 7, include_user_ids=[self_obj.user_uuid]
            )
            self.last_attack = time.time()
            self_obj.last_attack = time.time()

        if not self_obj.is_alive():
            return "dead"

        return STATE_CONTINUE


class DeadState(BaseState):
    DEAD_SECONDS = 20  # Enemy should stay 60 seconds dead

    def __init__(self, param: object):
        super().__init__(name="dead", param=param)

    def enter(self):
        self.death_ts = time.time()

    async def update(self, dt: float) -> str:
        self_obj = cast(PatrolEnemy, self.parameter)
        assert self_obj.user_uuid is not None

        if time.time() > self.death_ts + DeadState.DEAD_SECONDS:
            self_obj.health = self_obj.health_max
            return "patrol"

        return STATE_CONTINUE


class PatrolEnemy(Enemy):
    patrol_path: NPCPath
    speed: float

    def __init__(
        self, path: Polygon | None, speed: float, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)

        self.speed = speed

        self.patrol_path = NPCPath(path=path, speed=speed, loop=True)

        self.state_machine.add_state(PatrolState(self))
        self.state_machine.add_state(AggroState(self))
        self.state_machine.add_state(AttackingState(self))
        self.state_machine.add_state(DeadState(self))

        self.state_machine.change_state("patrol")


class BossPatrolEnemy(PatrolEnemy):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def take_damage(self, damage: int) -> None:
        self.health -= damage

        if self.user_uuid is None:
            return

        if self.health <= 0:
            success = await server.game_state.give_item(
                user_id=self.user_uuid,
                item=ITEMS["flag_boss"],
                once=True,
            )
            if success:
                await server.global_server.update_self(self.user_uuid)
