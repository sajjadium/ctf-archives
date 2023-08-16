import json
import math
import time
from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Literal, cast

from aiochclient import ChClient
from aiohttp import ClientSession
from aiohttp_retry import ExponentialRetry, RetryClient

import server
from server.game.entity.area import AreaObject
from server.game.entity.enemy import Enemy
from server.game.entity.npc import NPC
from server.game.entity.object import Object
from server.game.entity.pickupable import Pickupable
from server.game.fight import FightManager
from server.game.map.map import Map
from server.game.secret import ITEMS
from server.models import Position, ScoreboardEntry, Session
from shared.collison import CollisionManager, point_in_poly
from shared.constants import (
    CHUNK_SIZE_X,
    CHUNK_SIZE_Y,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    START_X,
    START_Y,
    TILE_SIZE_X,
    TILE_SIZE_Y,
    VIEW_DISTANCE_SQ,
)
from shared.gen.messages.v1 import (
    Coords,
    Item,
    Ping,
    SessionType,
    ShopInteract,
    ShopInteractType,
    User,
)


def sign(x: float) -> Literal[-1, 1, 0]:
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


class PrefixMatch:
    index: int
    expected: List[Any]

    def __init__(self, expected: List[Any]):
        self.index = 0
        self.expected = expected

    def check_next(self, obj: Any) -> bool:
        if self.expected[self.index] == obj:
            self.index += 1
            if self.index == len(self.expected):
                self.index = 0
                return True
        elif self.index > 0 and self.expected[self.index - 1] != obj:
            self.index = 0

        return False


class ObjectManager:
    static_objects: Dict[str, Object]

    def __init__(self):
        self.static_objects = {}

    def get_objects_dict(self) -> Dict[str, Object]:
        return self.static_objects

    def get_objects_list(self) -> List[Object]:
        return list(self.static_objects.values())

    def get_object_by_uuid(self, uuid: str) -> Object | None:
        if not uuid in self.static_objects:
            return None

        return self.static_objects[uuid]

    async def update(self, dt: float):
        for object in self.static_objects.values():
            await object.update(dt=dt)


class EnemyManager:
    enemies: Dict[str, Dict[str, Enemy]]
    object_manager: ObjectManager

    def __init__(self, object_manager: ObjectManager):
        self.enemies = defaultdict(lambda: {})
        self.object_manager = object_manager

    # Helper classes
    def get_enemies_for_user_dict(self, user_uuid: str) -> Dict[str, Enemy]:
        return self.enemies[user_uuid]

    def get_enemies_for_user_list(self, user_uuid: str) -> List[Enemy]:
        return list(self.enemies[user_uuid].values())

    def get_enemy_for_user_by_uuid(
        self, user_uuid: str, enemy_uuid: str
    ) -> Enemy | None:
        if not user_uuid in self.enemies:
            return None

        if not enemy_uuid in self.enemies[user_uuid]:
            return None

        return self.enemies[user_uuid][enemy_uuid]

    def new_login(self, user_uuid: str):
        if user_uuid not in self.enemies:
            self.enemies[user_uuid] = {}

    def deepcopy_add(self, user_uuid: str, enemy: Enemy):
        tmp = deepcopy(enemy)
        tmp.user_uuid = user_uuid

        self.enemies[user_uuid][enemy.uuid] = tmp

    async def update(self, dt: float):
        for _, user_enemies in self.enemies.items():
            for enemy in user_enemies.values():
                await enemy.update(dt)


class AreaManager:
    area_objects: Dict[str, Dict[str, AreaObject]]
    object_manager: ObjectManager

    def __init__(self, object_manager: ObjectManager):
        self.area_objects = defaultdict(lambda: {})
        self.object_manager = object_manager

    def get_areas_for_user_dict(self, user_uuid: str) -> Dict[str, AreaObject]:
        return self.area_objects[user_uuid]

    def get_areas_for_user_list(self, user_uuid: str) -> List[AreaObject]:
        return list(self.area_objects[user_uuid].values())

    async def update(self, dt: float):
        for user_areas in self.area_objects.values():
            for npc in user_areas.values():
                await npc.update(dt=dt)

    def get_areas_for_user_by_uuid(
        self, user_uuid: str, area_uuid: str
    ) -> AreaObject | None:
        if not user_uuid in self.area_objects:
            return None

        if not area_uuid in self.area_objects[user_uuid]:
            return None

        return self.area_objects[user_uuid][area_uuid]

    def deepcopy_add(self, user_uuid: str, area: AreaObject):
        tmp = deepcopy(area)
        tmp.user_uuid = user_uuid

        self.area_objects[user_uuid][area.uuid] = tmp


class NPCManager:
    npc_objects: Dict[str, Dict[str, NPC]]
    object_manager: ObjectManager

    def __init__(self, object_manager: ObjectManager):
        self.npc_objects = defaultdict(lambda: {})
        self.object_manager = object_manager

    def get_npcs_for_user_dict(self, user_uuid: str) -> Dict[str, NPC]:
        return self.npc_objects[user_uuid]

    def get_npcs_for_user_list(self, user_uuid: str) -> List[NPC]:
        return list(self.npc_objects[user_uuid].values())

    async def update(self, dt: float):
        for user_npcs in self.npc_objects.values():
            for npc in user_npcs.values():
                await npc.update(dt=dt)

    def get_npc_for_user_by_uuid(self, user_uuid: str, npc_uuid: str) -> NPC | None:
        if not user_uuid in self.npc_objects:
            return None

        if not npc_uuid in self.npc_objects[user_uuid]:
            return None

        return self.npc_objects[user_uuid][npc_uuid]

    def deepcopy_add(self, user_uuid: str, npc: NPC):
        tmp = deepcopy(npc)
        tmp.user_uuid = user_uuid

        self.npc_objects[user_uuid][npc.uuid] = tmp


class PickupableManager:
    pickupable_objects: Dict[str, Dict[str, Pickupable]]
    object_manager: ObjectManager

    def __init__(self, object_manager: ObjectManager):
        self.pickupable_objects = defaultdict(lambda: {})
        self.object_manager = object_manager

    def get_pickupable_for_user_dict(self, user_uuid: str) -> Dict[str, Pickupable]:
        return self.pickupable_objects[user_uuid]

    def get_pickupable_for_user_list(self, user_uuid: str) -> List[Pickupable]:
        return list(self.pickupable_objects[user_uuid].values())

    def get_pickupable_for_user_by_uuid(
        self, user_uuid: str, pickupable_uuid: str
    ) -> Pickupable | None:
        if not user_uuid in self.pickupable_objects:
            return None

        if not pickupable_uuid in self.pickupable_objects[user_uuid]:
            return None

        return self.pickupable_objects[user_uuid][pickupable_uuid]

    def deepcopy_add(self, user_uuid: str, pickupable: Pickupable) -> None:
        tmp = deepcopy(pickupable)
        tmp.user_uuid = user_uuid

        self.pickupable_objects[user_uuid][pickupable.uuid] = tmp

    async def update(self, dt: float) -> None:
        for _, pickupables in self.pickupable_objects.items():
            for pickupable in list(pickupables.values()):
                if pickupable.pickedup and pickupable.garbage_collect_on_pickup:
                    del pickupables[pickupable.uuid]
                    continue

                await pickupable.update(dt)


class Game:
    peer_sessions: Dict[str, Session]
    user_sessions: Dict[str, Session]
    users: Dict[str, User]
    recent_moves: Dict[str, PrefixMatch]
    user_collision_manager: CollisionManager
    objects: Dict[str, Dict[str, Object]]
    fight_manager: FightManager
    scoreboard: dict[str, ScoreboardEntry]
    running_scoreboard: dict[str, ScoreboardEntry]

    enemy_manager: EnemyManager
    object_manager: ObjectManager
    npc_manager: NPCManager
    area_manager: AreaManager
    pickupable_manager: PickupableManager

    def __init__(self) -> None:
        self.peer_sessions = {}
        self.user_sessions = {}
        self.users = {}
        self.recent_moves = {}

        self.user_collision_manager = CollisionManager(PLAYER_WIDTH, PLAYER_HEIGHT)

        # Manager
        self.fight_manager = FightManager()
        self.object_manager = ObjectManager()
        self.enemy_manager = EnemyManager(self.object_manager)
        self.npc_manager = NPCManager(self.object_manager)
        self.area_manager = AreaManager(self.object_manager)
        self.pickupable_manager = PickupableManager(self.object_manager)

        self.map = Map(Path(server.PATH, "./map/testmap.json"))
        self.object_manager.static_objects = self.map.initialize()

        self.scoreboard = {}
        self.running_scoreboard = {}

    async def init(self, clickhouse_url: str) -> None:
        self.session = ClientSession()
        retry_options = ExponentialRetry(attempts=2)
        self.retry_client = RetryClient(
            client_session=self.session, retry_options=retry_options
        )
        self.ch_client = ChClient(session=self.session, url=clickhouse_url)

    async def update_remote_user(self, user: User) -> None:
        session = self.user_sessions[user.uuid]

        await self.ch_client.execute(
            "INSERT INTO game.users VALUES",
            (
                user.uuid,
                user.username,
                user.coords.x,
                user.coords.y,
                user.coords.rotation,
                user.money,
                json.dumps([i.to_json() for i in user.inventory]),
                user.health,
                user.last_death,
                session.last_ping.timestamp(),
            ),
        )

    async def update_scoreboard(self, entry: ScoreboardEntry) -> None:
        user = self.users[entry.user_id]

        if entry.start is None:
            return

        if entry.end is None:
            return

        await self.ch_client.execute(
            "INSERT INTO game.scoreboard VALUES",
            (
                user.username,
                entry.start.timestamp(),
                entry.end.timestamp(),
            ),
        )

    async def get_remote_scoreboard(self) -> list[ScoreboardEntry]:
        res = await self.ch_client.fetch(
            "SELECT uuid, username, start, end FROM game.scoreboard FINAL INNER JOIN (SELECT * FROM game.users FINAL) users USING username"
        )

        return [
            ScoreboardEntry(
                user_id=r["uuid"],
                username=r["username"],
                start=datetime.fromtimestamp(r["start"]),
                end=datetime.fromtimestamp(r["end"]),
            )
            for r in res
        ]

    def is_authenticated(self, client: str) -> bool:
        return client in self.peer_sessions

    def is_logged_in(self, username: str) -> bool:
        return next(
            (
                True
                for u in self.user_sessions.keys()
                if self.users[u].username == username
            ),
            False,
        )

    async def is_logged_in_remote(self, username: str) -> bool:
        online_time = datetime.now() - timedelta(minutes=1)

        user = await self.ch_client.fetchrow(
            "SELECT * FROM game.users FINAL WHERE username = {username} AND last_ping >= {last_ping}",
            params={"username": username, "last_ping": online_time.timestamp()},
        )

        return user is not None

    def get_user_uuid(self, username: str) -> str | None:
        return next(
            (u.uuid for u in self.users.values() if u.username == username), None
        )

    def get_user(self, uuid: str | None) -> User | None:
        if uuid is None:
            return None

        return self.users[uuid]

    def get_session(self, user_id: str) -> str | None:
        return self.user_sessions[user_id].peer

    async def login(
        self, client: str, user_id: str, user: User, type: SessionType
    ) -> Session:
        await self.ch_client.is_alive()

        chunk_x = user.coords.x // (CHUNK_SIZE_X * TILE_SIZE_X)
        chunk_y = user.coords.y // (CHUNK_SIZE_Y * TILE_SIZE_Y)

        if self.map.is_dynamic_chunk(chunk_x, chunk_y):
            user.coords = Coords(x=START_X, y=START_Y)
            user.coords.timestamp = datetime.now()

        session = Session(peer=client, user_id=user_id, type=type)
        session.last_ping = datetime.now()
        self.peer_sessions[client] = session
        self.user_sessions[user_id] = session

        if user_id not in self.users:
            self.users[user_id] = user
            self.recent_moves[user_id] = PrefixMatch(
                [
                    (-1, 0),
                    (1, 0),
                    (1, -1),
                    (0, -1),
                    (-1, 1),
                    (0, -1),
                    (1, -1),
                    (-1, 0),
                    (1, 1),
                    (1, -1),
                    (0, -1),
                    (1, 0),
                ]
            )

        await self.update_remote_user(user)

        return session

    async def logout(self, client: str) -> None:
        if client in self.peer_sessions:
            session = self.peer_sessions[client]
            session.logout = True

            user = self.users[session.user_id]

            session.last_ping = datetime.fromtimestamp(0)
            await self.update_remote_user(user)

            self.peer_sessions.pop(client)
            self.user_sessions.pop(session.user_id)
            self.users.pop(session.user_id)

    async def move(self, client: str, coords: Coords) -> bool:
        if client in self.peer_sessions:
            session = self.peer_sessions[client]
            user_id = session.user_id
            user = self.users[user_id]

            if session.type == SessionType.SESSION_TYPE_FREE_CAM:
                user.coords = coords
                return True

            user_coords_timestamp = cast(datetime, user.coords.timestamp)  # type: ignore
            coords_timestamp = cast(datetime, coords.timestamp)  # type: ignore

            distance_time = coords_timestamp - user_coords_timestamp
            distance_x = user.coords.x - coords.x
            distance_y = user.coords.y - coords.y

            distance_sq = distance_x**2 + distance_y**2

            max_distance_sq = (
                min(distance_time.total_seconds(), 0.2) * PLAYER_SPEED
            ) ** 2

            if max_distance_sq < distance_sq:
                # maybe we found a hacker, check average over last positions

                check_time = 0.2  # check for the last 200 ms
                new_pos: list[Position] = []
                k = -1
                while len(session.last_positions) > 0:
                    pos = session.last_positions.pop()
                    new_pos.append(pos)
                    k = (coords_timestamp - pos.time).total_seconds()
                    if k >= check_time:
                        break
                toff = (
                    coords_timestamp - new_pos[-1].time
                ).total_seconds() - check_time
                session.last_positions = new_pos[::-1]
                if len(new_pos) < 2:
                    user.coords.timestamp = coords_timestamp
                    return False

                # does this interpolation to exactly 0.2s anything? or would comparison to 0.2+toff also be fine?
                dt = (new_pos[-2].time - new_pos[-1].time).total_seconds()
                dx = (new_pos[-2].coords.x - new_pos[-1].coords.x) * (toff / dt)
                dy = (new_pos[-2].coords.y - new_pos[-1].coords.y) * (toff / dt)

                pos_at_50 = new_pos[-1].coords.x + dx, new_pos[-1].coords.y + dy
                distance_x_at_50 = coords.x - pos_at_50[0]
                distance_y_at_50 = coords.y - pos_at_50[1]
                distance_sq_50 = distance_x_at_50**2 + distance_y_at_50**2
                # with this change PLAYER_SPEED (not *1.2) should be fine, but it isn't, why?
                #
                if math.sqrt(distance_sq_50) > check_time * PLAYER_SPEED * 1.2:
                    print(distance_time.total_seconds())
                #    print(math.sqrt(distance_sq_50), check_time * PLAYER_SPEED, k)
                if math.sqrt(distance_sq_50) > check_time * PLAYER_SPEED * 1.2:
                    user.coords.timestamp = coords_timestamp
                    return False

            match self.user_collision_manager.check_collisons(
                self.map, user.coords.x, user.coords.y, coords.x, coords.y, user_id
            ):
                case None:
                    return False
                case x, y:
                    pass

            valid = True
            if x != coords.x or y != coords.y:
                valid = False
                coords.x = x
                coords.y = y

            user.coords = coords

            if valid:
                await self.update_remote_user(user)

                session.last_positions.append(Position(coords, coords_timestamp))

                if self.recent_moves[user_id].check_next(
                    (sign(distance_x), sign(distance_y))
                ):
                    await self.give_item(
                        user_id,
                        ITEMS["flag_cheat"],
                        True,
                    )

            return valid

        return False

    async def give_item(self, user_id: str, item: Item, once: bool = False) -> bool:
        user = self.users[user_id]

        res = True

        for i in user.inventory:
            if i.name == item.name:
                if once:
                    res = False

                    break
                else:
                    i.quantity += item.quantity
                    res = True

                    break
        else:
            user.inventory.append(item)

        if res:
            await server.global_server.update_self(user_id)

        return res

    def shop(self, user_id: str, shop_interact: ShopInteract) -> bool:
        user = self.users[user_id]

        match shop_interact.type:
            case ShopInteractType.SHOP_INTERACT_TYPE_BUY:
                item = None
                for i in user.inventory:
                    if i.name == shop_interact.item.name:
                        item = i

                        break
                else:
                    return False

                if item.quantity >= shop_interact.item.quantity:
                    item.quantity -= shop_interact.item.quantity

                    if item.quantity == 0:
                        user.inventory.remove(item)

                    user.money += shop_interact.cost

                    return True

            case ShopInteractType.SHOP_INTERACT_TYPE_SELL:
                if user.money >= shop_interact.cost:
                    user.money -= shop_interact.cost

                    for i in user.inventory:
                        if i.name == shop_interact.item.name:
                            i.quantity += shop_interact.item.quantity

                            break
                    else:
                        user.inventory.append(shop_interact.item)

                    return True

            case ShopInteractType.SHOP_INTERACT_TYPE_TRADE:
                item = None
                for i in user.inventory:
                    if i.name == shop_interact.item.name:
                        item = i

                        break
                else:
                    return False

                if item.quantity >= shop_interact.item.quantity:
                    item.quantity -= shop_interact.item.quantity

                    if item.quantity == 0:
                        user.inventory.remove(item)

                    for i in user.inventory:
                        if i.name == shop_interact.trade_in.name:
                            i.quantity += shop_interact.trade_in.quantity

                            break
                    else:
                        user.inventory.append(shop_interact.trade_in)

                    return True
            case _:
                pass

        return False

    def get_users(self, client: str | None = None) -> List[User]:
        if client in self.peer_sessions:
            return [u for c, u in self.users.items() if c != self.peer_sessions[client]]

        return list(self.users.values())

    def get_online_users(self, client: str | None = None) -> List[User]:
        if client in self.peer_sessions:
            return [
                self.users[user_id]
                for user_id, session in self.user_sessions.items()
                if session.peer != client
                and session.type != SessionType.SESSION_TYPE_FREE_CAM
            ]

        return list(self.users.values())

    async def get_remote_username(self, username: str) -> User | None:
        user = await self.ch_client.fetchrow(
            "SELECT uuid, username, x, y, rotation FROM game.users FINAL WHERE username = {username}",
            params={"username": username},
        )

        if user:
            return User(
                uuid=str(user["uuid"]),
                username=user["username"],
                last_death=user["last_death"],
                coords=Coords(x=user["x"], y=user["y"], rotation=user["rotation"]),
            )
        else:
            return None

    async def get_remote_userid(self, user_id: str) -> User | None:
        user = await self.ch_client.fetchrow(
            "SELECT uuid, username, x, y, rotation, last_death FROM game.users FINAL WHERE uuid = {uuid}",
            params={"uuid": user_id},
        )

        if user:
            return User(
                uuid=str(user["uuid"]),
                username=user["username"],
                last_death=user["last_death"],
                coords=Coords(x=user["x"], y=user["y"], rotation=user["rotation"]),
            )
        else:
            return None

    async def get_remote_fulluser(self, username: str) -> User | None:
        user = await self.ch_client.fetchrow(
            "SELECT * FROM game.users FINAL WHERE username = {username}",
            params={"username": username},
        )

        if user:
            return User(
                uuid=str(user["uuid"]),
                username=user["username"],
                coords=Coords(x=user["x"], y=user["y"], rotation=user["rotation"]),
                money=user["money"],
                inventory=[Item().from_json(i) for i in json.loads(user["inventory"])],
                health=user["health"],
                last_death=user["last_death"],
            )
        else:
            return None

    async def get_remote_online_users(
        self, exclude_user_id: str | None = None
    ) -> List[User]:
        online_time = datetime.now() - timedelta(minutes=1)

        res = []
        if exclude_user_id is None:
            res = await self.ch_client.fetch(
                "SELECT uuid, username, x, y, rotation, last_death FROM game.users FINAL WHERE last_ping >= {last_ping}",
                params={"last_ping": online_time.timestamp()},
            )
        else:
            res = await self.ch_client.fetch(
                "SELECT uuid, username, x, y, rotation, last_death FROM game.users FINAL WHERE uuid != {uuid} AND last_ping >= {last_ping}",
                params={"uuid": exclude_user_id, "last_ping": online_time.timestamp()},
            )

        users = [
            User(
                uuid=str(r["uuid"]),
                username=r["username"],
                last_death=r["last_death"],
                coords=Coords(x=r["x"], y=r["y"], rotation=r["rotation"]),
            )
            for r in res
        ]

        return users

    def get_local_users_distance(
        self, x: float, y: float, user_session: Session | None = None
    ) -> List[User]:
        peer = None
        if user_session:
            peer = user_session.peer

        users = self.get_online_users(peer)

        objects = filter(
            lambda e: (abs(x - e.coords.x) ** 2) + (abs(y - e.coords.y) ** 2)
            <= VIEW_DISTANCE_SQ,
            users,
        )

        return list(objects)

    async def get_online_users_distance(
        self, x: float, y: float, user_session: Session | None = None
    ) -> List[User]:
        peer = None
        user_id = None
        if user_session:
            peer = user_session.peer
            user_id = user_session.user_id

        users = self.get_online_users(peer) + await self.get_remote_online_users(
            user_id
        )

        objects = filter(
            lambda e: (abs(x - e.coords.x) ** 2) + (abs(y - e.coords.y) ** 2)
            <= VIEW_DISTANCE_SQ,
            users,
        )

        return list(objects)

    @staticmethod
    def is_in_view(x: float, y: float, object: Object) -> bool:
        match object:
            case AreaObject():
                return point_in_poly(x, y, object.area)
            case _:
                return ((x - object.x) ** 2) + ((y - object.y) ** 2) <= VIEW_DISTANCE_SQ

    def get_objects_view_distance(self, uuid: str, x: float, y: float) -> List[Object]:
        original_objects = filter(
            lambda obj: self.is_in_view(x, y, obj),
            self.object_manager.get_objects_list(),
        )

        # A list to store all the different object types as Object
        objects: Dict[str, Object] = {}
        # Get map values. Those are Enemies, NPCs, Items etc. Depending on the type, we have to handle them per user
        # TODO: Maybe better perf to add the deepcopied object directly
        for o in original_objects:
            match o:
                case AreaObject():
                    if o.uuid not in self.area_manager.get_areas_for_user_dict(
                        user_uuid=uuid
                    ):
                        self.area_manager.deepcopy_add(user_uuid=uuid, area=o)

                    objects[o.uuid] = self.area_manager.get_areas_for_user_dict(
                        user_uuid=uuid
                    )[o.uuid]
                case NPC():
                    if o.interactable:
                        if o.uuid not in self.npc_manager.get_npcs_for_user_dict(
                            user_uuid=uuid
                        ):
                            self.npc_manager.deepcopy_add(user_uuid=uuid, npc=o)

                        objects[o.uuid] = self.npc_manager.get_npcs_for_user_dict(
                            user_uuid=uuid
                        )[o.uuid]
                    else:
                        objects[o.uuid] = o
                case Enemy():
                    if o.uuid not in self.enemy_manager.get_enemies_for_user_dict(
                        user_uuid=uuid
                    ):
                        self.enemy_manager.deepcopy_add(user_uuid=uuid, enemy=o)

                    objects[o.uuid] = self.enemy_manager.get_enemies_for_user_dict(
                        user_uuid=uuid
                    )[o.uuid]
                case Pickupable():
                    if o.pickedup:
                        continue

                    if (
                        o.uuid
                        not in self.pickupable_manager.get_pickupable_for_user_dict(
                            user_uuid=uuid
                        )
                    ):
                        self.pickupable_manager.deepcopy_add(
                            user_uuid=uuid, pickupable=o
                        )

                    object = self.pickupable_manager.get_pickupable_for_user_dict(
                        user_uuid=uuid
                    )[o.uuid]

                    if not object.pickedup:
                        objects[o.uuid] = object
                # Fallback for unknown objects
                case _:
                    objects[o.uuid] = o

        objects.update(
            {
                p.uuid: p
                for p in self.area_manager.get_areas_for_user_list(user_uuid=uuid)
                if p.uuid not in objects
            }
        )

        objects.update(
            {
                p.uuid: p
                for p in self.npc_manager.get_npcs_for_user_list(user_uuid=uuid)
                if p.uuid not in objects
            }
        )

        objects.update(
            {
                p.uuid: p
                for p in self.enemy_manager.get_enemies_for_user_list(user_uuid=uuid)
                if p.uuid not in objects
            }
        )

        objects.update(
            {
                p.uuid: p
                for p in self.pickupable_manager.get_pickupable_for_user_list(
                    user_uuid=uuid
                )
                if p.uuid not in objects and not p.pickedup
            }
        )
        # objects += self.object_manager.get_static_objects()

        return list(objects.values())

    def start_timer(self, user_id: str) -> None:
        scoreboard_entry = self.running_scoreboard.get(user_id)

        if scoreboard_entry is None:
            scoreboard_entry = ScoreboardEntry(user_id=user_id)
            self.running_scoreboard[user_id] = scoreboard_entry

        scoreboard_entry.reset()
        scoreboard_entry.start = datetime.now()

    async def stop_timer(self, user_id: str) -> ScoreboardEntry | None:
        scoreboard_entry = self.running_scoreboard.get(user_id)

        if scoreboard_entry is None:
            return

        if scoreboard_entry.end:
            return

        scoreboard_entry.end = datetime.now()
        del self.running_scoreboard[user_id]

        last_best_entry = self.scoreboard.get(user_id)

        if last_best_entry is None or last_best_entry.time > scoreboard_entry.time:
            self.scoreboard[user_id] = scoreboard_entry

            await self.update_scoreboard(scoreboard_entry)

        return scoreboard_entry

    async def die(self, user: User) -> None:
        print(f"Player {user.username} died :( Resetting")
        user.last_death = time.time()
        start_coords = Coords(x=START_X, y=START_Y)
        start_coords.timestamp = datetime.now()
        user.health = 100
        user.coords = start_coords

        await self.update_remote_user(user)

    async def ping(self, peer: str, ping: Ping) -> None:
        session = self.peer_sessions[peer]

        if session.logout:
            return

        user = self.users[session.user_id]

        session.last_ping = datetime.now()

        await self.update_remote_user(user)
