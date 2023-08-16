from __future__ import annotations

import struct
import time
import traceback
from asyncio import (
    Queue,
    StreamReader,
    StreamWriter,
    as_completed,
    create_task,
    sleep,
    start_server,
)
from copy import deepcopy
from datetime import datetime, timedelta
from threading import Event
from typing import Awaitable, Callable, Dict, Tuple, TypeVar, cast
from uuid import uuid4

from betterproto import which_one_of

import server
from server.game.auth import auth
from server.game.entity.area import AreaObject
from server.game.entity.enemy import Enemy
from server.game.entity.npc import NPC
from server.game.map.properties import CustomInteraction, InteractionOn
from shared.collison import point_in_poly
from shared.constants import PLAYER_DEATH_TIMEOUT, SERVER_TICK_RATE, START_X, START_Y
from shared.gen.messages.v1 import (
    AcknowledgeDamage,
    AttackEnemy,
    ClientMessage,
    Coords,
    EnemyInfo,
    Error,
    ErrorType,
    GiveDamage,
    Interact,
    InteractStatus,
    InteractType,
    LoggedIn,
    Login,
    Logout,
    MapChunkRequest,
    MapChunkResponse,
    Object,
    ObjectAsset,
    ObjectAssetRequest,
    Objects,
    ObjectType,
    Ping,
    ServerMessage,
    SessionType,
    User,
    Users,
)
from shared.utils import AsyncEventHandler

ServerMessageOneOfType = (
    Ping
    | Login
    | Coords
    | MapChunkRequest
    | ObjectAssetRequest
    | Interact
    | AcknowledgeDamage
    | AttackEnemy
    | Logout
)
ServerMessageOneOfTypeVar = TypeVar(
    "ServerMessageOneOfTypeVar",
    Ping,
    Login,
    Coords,
    MapChunkRequest,
    ObjectAssetRequest,
    Interact,
    AcknowledgeDamage,
    AttackEnemy,
    Logout,
)


class Connection:
    reader: StreamReader
    writer: StreamWriter

    # (ServerMessage, Handler)
    network_queue: Queue[
        Tuple[ServerMessage, Callable[[ServerMessageOneOfType], None] | None]
    ]
    handlers: Dict[str, Callable[[ServerMessageOneOfType], None]]

    peer: str

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

        self.network_queue = Queue()
        self.handlers = {}

        self.peer = reader._transport.get_extra_info("peername")  # type: ignore

        self.ping_handler = AsyncEventHandler([self._ping])
        self.login_handler = AsyncEventHandler([self._login])
        self.move_handler = AsyncEventHandler([self._move])
        self.map_chunk_handler = AsyncEventHandler([self._chunk_request])
        self.object_asset_handler = AsyncEventHandler([self._object_asset_request])
        self.interact_handler = AsyncEventHandler([self._interact])
        self.acknowledge_damage_handler = AsyncEventHandler([self._acknowledge_damage])
        self.attack_enemy_handler = AsyncEventHandler([self._attack_enemy])
        self.logout_handler = AsyncEventHandler([self._logout])

    async def read_message_loop(self) -> None:
        try:
            while not self.reader.at_eof():
                size_buf = await self.reader.readexactly(4)

                size = struct.unpack("!i", size_buf)[0]
                data_buf = await self.reader.readexactly(size)

                message = ClientMessage().parse(data_buf)
                message_id = message.uuid

                _, inner_message = which_one_of(message=message, group_name="message")

                match inner_message:
                    case Ping():
                        await self.ping_handler(message_id, inner_message)
                    case Login():
                        await self.login_handler(message_id, inner_message)
                    case Coords():
                        await self.move_handler(message_id, inner_message)
                    case MapChunkRequest():
                        await self.map_chunk_handler(message_id, inner_message)
                    case ObjectAssetRequest():
                        await self.object_asset_handler(message_id, inner_message)
                    case Interact():
                        await self.interact_handler(message_id, inner_message)
                    case AcknowledgeDamage():
                        await self.acknowledge_damage_handler(message_id, inner_message)
                    case AttackEnemy():
                        await self.attack_enemy_handler(message_id, inner_message)
                    case Logout():
                        await self.logout_handler(message_id, inner_message)
                    case default:
                        raise Exception(f"Unkown message_type: {default}")

        except Exception:
            traceback.print_exc()

            if server.game_state.is_authenticated(self.peer):
                await self.logout()

    async def send_message_loop(self) -> None:
        try:
            while True:
                message, handler = await self.network_queue.get()

                if message.uuid == "":
                    message_id = str(uuid4())
                    message.uuid = message_id

                if handler is not None:
                    self.handlers[message.uuid] = handler

                self._send_message(message)
        except Exception:
            traceback.print_exc()

            if server.game_state.is_authenticated(self.peer):
                await self.logout()

    def _send_message(self, client_message: ServerMessage) -> None:
        message_bytes = client_message.SerializeToString()

        message = struct.pack("!i", len(message_bytes)) + message_bytes
        self.writer.write(message)

    @staticmethod
    def authenticated(
        func: Callable[[Connection, str, ServerMessageOneOfTypeVar], Awaitable[None]]
    ) -> Callable[[Connection, str, ServerMessageOneOfTypeVar], Awaitable[None]]:
        async def inner(
            self: Connection, uuid: str, message: ServerMessageOneOfTypeVar
        ) -> None:
            if server.game_state.is_authenticated(self.peer):
                await func(self, uuid, message)
            else:
                response = ServerMessage(
                    error=Error(
                        type=ErrorType.ERROR_TYPE_UNAUTHORIZED,
                        message="Not logged in yet.",
                    ),
                    uuid=uuid,
                )

                await self.network_queue.put((response, None))

        return inner

    @authenticated
    async def _logout(self, uuid: str, message: Logout) -> None:
        await self.logout()

    async def logout(self) -> None:
        session = server.game_state.peer_sessions[self.peer]
        user = server.game_state.get_user(session.user_id)

        if user is None:
            return

        if session.type != SessionType.SESSION_TYPE_FREE_CAM:
            response = ServerMessage(logout=Logout(user=user))
            await server.global_server.broadcast(response)

        await server.game_state.logout(self.peer)

    @authenticated
    async def _ping(self, uuid: str, message: Ping) -> None:
        await server.game_state.ping(self.peer, message)

        response = ServerMessage(ping=Ping(time=datetime.now()), uuid=uuid)

        await self.network_queue.put((response, None))

    async def _login(self, uuid: str, message: Login) -> None:
        res = auth(message.username, message.password)
        error_msg = ErrorType.ERROR_TYPE_UNSPECIFIED

        if res == None:  # Invalid auth
            error_msg = ErrorType.ERROR_TYPE_UNAUTHORIZED

        user_uuid = server.game_state.get_user_uuid(message.username)
        user = server.game_state.get_user(user_uuid)

        if user is None:
            user = await server.game_state.get_remote_fulluser(message.username)

            if user:
                user.coords.timestamp = datetime.now()
        if user is None:
            user_id = str(uuid4())

            start_coords = Coords(x=START_X, y=START_Y)
            start_coords.timestamp = datetime.now()

            user = User(
                username=message.username,
                uuid=user_id,
                coords=start_coords,
                money=1000,
                health=100,
                last_death=0,
            )
        elif (
            user.last_death != 0
            and (time.time() - user.last_death)
            < PLAYER_DEATH_TIMEOUT  # Check if user is still in timeout
        ):
            res = None
            error_msg = ErrorType.ERROR_TYPE_TIMEOUT

        else:
            if server.game_state.is_logged_in(message.username):
                res = None
                error_msg = ErrorType.ERROR_TYPE_ALREADY_LOGGED_IN

            if await server.game_state.is_logged_in_remote(message.username):
                res = None
                error_msg = ErrorType.ERROR_TYPE_ALREADY_LOGGED_IN

        response = ServerMessage(
            logged_in=LoggedIn(
                success=res is not None,
                type=res if res is not None else SessionType.SESSION_TYPE_UNSPECIFIED,
                error=error_msg,
            ),
            uuid=uuid,
        )

        if res:
            response.logged_in.self = user
            response.logged_in.assets = server.game_state.map.player_asset
            response.logged_in.interact_distance = 14

        await self.network_queue.put((response, None))

        if res:
            await server.game_state.login(self.peer, user.uuid, user, res)

            if res != SessionType.SESSION_TYPE_FREE_CAM:
                response = ServerMessage(users=Users(users=[user]))
                await server.global_server.broadcast(response, exclude=[self.peer])

            users = server.game_state.get_online_users(self.peer)
            response = ServerMessage(
                users=Users(users=users),
            )
            await self.network_queue.put((response, None))

            await self._send_new_objects_view_distance(user)

    @authenticated
    async def _move(self, uuid: str, message: Coords) -> None:
        message.timestamp = datetime.now()

        valid = await server.game_state.move(self.peer, message)

        session = server.game_state.peer_sessions[self.peer]
        user_uuid = session.user_id
        user = server.game_state.get_user(user_uuid)

        if user is None:
            return

        await self._send_new_objects_view_distance(user)

        if session.type != SessionType.SESSION_TYPE_FREE_CAM:
            if not valid:
                response = ServerMessage(users=Users(users=[user]))
                await server.global_server.broadcast(response, include=[self.peer])

            objects = server.game_state.get_objects_view_distance(
                user_uuid, user.coords.x, user.coords.y
            )
            for o in objects:
                match o:
                    case AreaObject():
                        if o.interaction_on != InteractionOn.COLLIDE:
                            continue

                        if point_in_poly(user.coords.x, user.coords.y, o.area):
                            if not o.actice:
                                interact = o.in_range(user_uuid)
                                if interact:
                                    resp = ServerMessage()
                                    resp.interact = interact

                                    await server.global_server.broadcast(
                                        resp, include=[self.peer]
                                    )
                        elif o.actice:
                            interact = o.out_of_range(user_uuid)
                            if interact:
                                resp = ServerMessage()
                                resp.interact = interact

                                await server.global_server.broadcast(
                                    resp, include=[self.peer]
                                )
                    case _:
                        pass

    @authenticated
    async def _chunk_request(self, uuid: str, message: MapChunkRequest) -> None:
        session = server.game_state.peer_sessions[self.peer]

        chunks = server.game_state.map.get_chunks(message.x, message.y, session.user_id)

        response = ServerMessage(uuid=uuid)

        if len(chunks) == 0:
            response.error = Error(
                type=ErrorType.ERROR_TYPE_INVALID_CHUNK,
                message="Invalid Chunk requested",
            )

        else:
            print("Sending Chunk", chunks[0].x, chunks[0].y)

            response.chunk = MapChunkResponse(chunks=chunks)

        await self.network_queue.put((response, None))

    @authenticated
    async def _acknowledge_damage(self, uuid: str, message: AcknowledgeDamage) -> None:
        user_uuid = server.game_state.peer_sessions[self.peer].user_id
        user = server.game_state.get_user(uuid=user_uuid)

        if user is None:
            return

        response = ServerMessage(uuid=uuid)

        if (
            server.game_state.fight_manager.can_take_damage_user(
                username=user.username, cooldown_ticks=30
            )
            and message.damage > 0
        ):
            user.health -= message.damage

            await self.network_queue.put((response, None))

            await server.global_server.update_self(user.uuid)

    @authenticated
    async def _attack_enemy(self, uuid: str, message: AttackEnemy) -> None:
        session = server.game_state.peer_sessions[self.peer]

        if session.type != SessionType.SESSION_TYPE_NORMAL:
            return

        user = server.game_state.get_user(uuid=session.user_id)
        if user is None:
            print("User not found")
            return

        enemy = server.game_state.enemy_manager.get_enemy_for_user_by_uuid(
            user_uuid=session.user_id, enemy_uuid=message.uuid
        )

        if enemy is None:
            return  # TODO: Enemy not found message to client?

        if not server.game_state.fight_manager.is_plausible_attack(
            user=user, enemy=enemy, attack_msg=message
        ):
            print("not plausible attack")
            return  # TODO: Not plausible message to client?

        if not server.game_state.fight_manager.can_take_damage_enemy(
            enemy_uuid=enemy.uuid, cooldown_ticks=30
        ):  # TODO: Dynamic cooldown for attacks
            print("Enemy can't get damage again, cooldown not reached")
            return  # TODO: Not plausible message to client?

        await enemy.take_damage(message.damage)

        # We use `move_enemy_object` here to send the enemy update to the client. Lazy, but good enough
        await server.global_server.move_enemy_object(
            uuid=enemy.uuid,
            x=enemy.x,
            y=enemy.y,
            health=enemy.health,
            health_max=enemy.health_max,
            last_attack=enemy.last_attack,
            name=enemy.name,
            include_user_ids=[user.uuid],
        )

    @authenticated
    async def _object_asset_request(
        self, uuid: str, message: ObjectAssetRequest
    ) -> None:
        response = ServerMessage(uuid=uuid)

        o = server.game_state.object_manager.get_object_by_uuid(message.uuid)
        match o:
            case NPC():
                response.object_asset = ObjectAsset(
                    object_uuid=o.uuid,
                    assets=o.entity_assets,
                    name=o.name,
                    type=ObjectType.OBJECT_TYPE_NPC,
                    interactable=o.interactable,
                    interact_distance=o.interact_distance,
                )
            case Enemy():
                response.object_asset = ObjectAsset(
                    object_uuid=o.uuid,
                    assets=o.entity_assets,
                    name=o.name,
                    type=ObjectType.OBJECT_TYPE_ENEMY,
                    interactable=False,
                    interact_distance=0,
                )
            case _:
                if message.uuid in server.game_state.users:
                    response.object_asset = ObjectAsset(
                        object_uuid=message.uuid,
                        assets=server.game_state.map.player_asset,
                    )
                elif (
                    await server.game_state.get_remote_userid(message.uuid) is not None
                ):
                    response.object_asset = ObjectAsset(
                        object_uuid=message.uuid,
                        assets=server.game_state.map.player_asset,
                    )
                else:
                    response.error = Error(
                        type=ErrorType.ERROR_TYPE_INVALID_OBJECT,
                        message="Invalid Object requested",
                    )

        await self.network_queue.put((response, None))

    @authenticated
    async def _interact(self, uuid: str, message: Interact) -> None:
        response = ServerMessage(uuid=uuid)

        obj = server.game_state.object_manager.get_object_by_uuid(message.uuid)
        if obj is None:
            response.error = Error(
                type=ErrorType.ERROR_TYPE_INVALID_OBJECT,
                message="Invalid Object requested",
            )
        else:
            session = server.game_state.peer_sessions[self.peer]
            user_id = session.user_id

            if session.type != SessionType.SESSION_TYPE_NORMAL:
                return

            user = server.game_state.get_user(user_id)
            match obj:
                case AreaObject():
                    o = server.game_state.area_manager.get_areas_for_user_by_uuid(
                        user_uuid=user_id, area_uuid=message.uuid
                    )

                    if user is None or o is None:
                        response.error = Error(
                            type=ErrorType.ERROR_TYPE_INVALID_OBJECT,
                            message="Invalid Object requested",
                        )
                    else:
                        if o.interaction_on != InteractionOn.INTERACT:
                            response.error = Error(
                                type=ErrorType.ERROR_TYPE_INVALID_OBJECT,
                                message="Invalid interaction requested",
                            )
                        else:
                            if point_in_poly(user.coords.x, user.coords.y, o.area):
                                interact = await o.interact(user_id, message)
                                if not interact:
                                    response.error = Error(
                                        type=ErrorType.ERROR_TYPE_INVALID_OBJECT,
                                        message="Invalid interaction requested",
                                    )
                                else:
                                    response.interact = interact
                case NPC():
                    o = server.game_state.npc_manager.get_npc_for_user_by_uuid(
                        user_uuid=user_id, npc_uuid=message.uuid
                    )
                    player_asset = server.game_state.map.player_asset

                    if user is None or o is None:
                        response.error = Error(
                            type=ErrorType.ERROR_TYPE_INVALID_OBJECT,
                            message="Invalid Object requested",
                        )
                    else:
                        if not o.interactable:
                            return

                        dx = (user.coords.x + player_asset.width / 2) - (
                            (o.x + o.entity_assets.width / 2)
                        )
                        dy = (user.coords.y - player_asset.height / 2) - (
                            (o.y - o.entity_assets.height / 2)
                        )
                        distance_sq = dx**2 + dy**2

                        if distance_sq < (o.interact_distance + 14) ** 2:
                            status = message.status
                            text = ""
                            interaction_type = InteractType.INTERACT_TYPE_UNSPECIFIED
                            shop = []
                            progress = 0.0

                            if (
                                o.interactions[o.interaction_step].custom_interaction
                                == CustomInteraction.RUNNER
                            ):
                                interaction = await o.interact(
                                    user_id=user_id, interact=message
                                )
                                if o.runner_seed is not None:
                                    progress = o.runner_seed
                                interaction_type = interaction.interaction_type

                            elif message.status != InteractStatus.INTERACT_STATUS_STOP:
                                interaction = await o.interact(
                                    user_id=user_id, interact=message
                                )

                                text = await interaction.text
                                shop = interaction.shop

                                if (
                                    text == ""
                                    and len(shop) == 0
                                    and interaction.interaction_type
                                    != InteractType.INTERACT_TYPE_RUNNER
                                ):
                                    status = InteractStatus.INTERACT_STATUS_STOP

                                interaction_type = interaction.interaction_type

                                for s in shop:
                                    if s.item:
                                        s.item.description = ""

                                    if s.trade_in:
                                        s.trade_in.description = ""

                            response.interact = Interact(
                                status=status,
                                uuid=message.uuid,
                                text=text,
                                type=interaction_type,
                                shop=shop,
                                progress=progress,
                            )
                case _:
                    response.error = Error(
                        type=ErrorType.ERROR_TYPE_INVALID_OBJECT,
                        message="Invalid Object requested",
                    )

        await self.network_queue.put((response, None))

    async def _send_new_objects_view_distance(self, user: User) -> None:
        objects: list[Object] = []
        session = server.game_state.user_sessions[user.uuid]

        for e in server.game_state.get_objects_view_distance(
            uuid=user.uuid, x=user.coords.x, y=user.coords.y
        ):
            if e.uuid in session.known_objects:
                continue

            obj_to_add = e.to_proto()
            if e.type == ObjectType.OBJECT_TYPE_PICKUPABLE:
                obj_to_add = deepcopy(obj_to_add)
                obj_to_add.pickupable.description = ""

            assert obj_to_add.type != ObjectType.OBJECT_TYPE_UNSPECIFIED, obj_to_add
            objects.append(obj_to_add)

        if len(objects) > 0:
            session.known_objects |= set([o.uuid for o in objects])
            response = ServerMessage(
                objects=Objects(objects=objects),
            )
            await self.network_queue.put((response, None))


class Server:
    connections: Dict[str, Connection]

    def __init__(self, clickhouse_url: str) -> None:
        self.connections = {}
        self.clickhouse_url = clickhouse_url

    async def start(self, host: str, port: int, running: Event) -> None:
        self.running = running

        await server.game_state.init(self.clickhouse_url)

        s = await start_server(self.hande_cb, host=host, port=port)
        update_loop_task = create_task(self.update_loop())

        for coro in as_completed([update_loop_task]):
            await coro

            running.clear()
            break

        s.close()

    # This is needed to give execution back to the control loop during the connection awaits
    async def update_loop(self) -> None:
        last_time = datetime.now()

        while self.running.is_set():
            current_time = datetime.now()
            dt = (current_time - last_time).total_seconds()

            if dt > (1 / (SERVER_TICK_RATE)) * 1.2:
                print("REEE Server Lag")

            await server.game_state.npc_manager.update(dt=dt)
            await server.game_state.enemy_manager.update(dt=dt)
            await server.game_state.pickupable_manager.update(dt=dt)
            await server.game_state.object_manager.update(dt=dt)

            # Check for user death and set timeout
            for user in server.game_state.users.values():
                if user.health < 0:
                    await server.game_state.die(user)

                    if user.uuid in server.game_state.user_sessions:
                        peer = server.game_state.user_sessions[user.uuid].peer
                        if (
                            peer in server.global_server.connections
                            and server.game_state.is_authenticated(peer)
                        ):
                            await server.global_server.connections[peer].logout()

            online_time = current_time - timedelta(minutes=1)
            for s in list(server.game_state.peer_sessions.values()):
                if s.last_ping.timestamp() < online_time.timestamp():
                    await server.global_server.connections[s.peer].logout()

            await self.update_other_player_position()

            last_time = datetime.now()
            await sleep(1 / SERVER_TICK_RATE)

    async def hande_cb(self, reader: StreamReader, writer: StreamWriter) -> None:
        connection = Connection(reader, writer)

        peer = cast(str, reader._transport.get_extra_info("peername"))  # type: ignore

        self.connections[peer] = connection

        read_task = create_task(connection.read_message_loop())
        send_task = create_task(connection.send_message_loop())

        for coro in as_completed([read_task, send_task]):
            await coro

            break

        del self.connections[peer]

    def broadcast_sync(
        self,
        message: ServerMessage,
        handler: Callable[[ServerMessageOneOfType], None] | None = None,
        exclude: list[str] = [],
        include: list[str] | None = None,
    ) -> None:
        for peer, c in self.connections.items():
            if not server.game_state.is_authenticated(peer):
                continue

            if peer in exclude:
                continue

            if include is not None and peer not in include:
                continue

            c.network_queue.put_nowait((message, handler))

    async def broadcast(
        self,
        message: ServerMessage,
        handler: Callable[[ServerMessageOneOfType], None] | None = None,
        exclude: list[str] = [],
        include: list[str] | None = None,
    ) -> None:
        for peer, c in self.connections.items():
            if not server.game_state.is_authenticated(peer):
                continue

            if peer in exclude:
                continue

            if include is not None and peer not in include:
                continue

            await c.network_queue.put((message, handler))

    async def move_object(
        self,
        uuid: str,
        x: float,
        y: float,
        include_user_ids: list[str] | None = None,
    ) -> None:
        # No type specified, as this should be an object already known to the client
        r = ServerMessage(objects=Objects([Object(uuid=uuid, coords=Coords(x=x, y=y))]))

        users = server.game_state.get_local_users_distance(x, y)
        users = [u.uuid for u in users]

        if include_user_ids is not None:
            users = [u for u in users if u in include_user_ids]

        users_sessions = [
            server.game_state.user_sessions[u].peer
            for u in users
            if u in server.game_state.user_sessions
        ]

        if len(users_sessions) == 0:
            return

        await self.broadcast(r, include=users_sessions)

    # This also includes enemy specific information
    async def move_enemy_object(
        self,
        uuid: str,
        x: float,
        y: float,
        health: int,
        health_max: int,
        last_attack: float,
        name: str,
        include_user_ids: list[str] | None = None,
    ) -> None:
        # No type specified, as this should be an object already known to the client
        r = ServerMessage(
            objects=Objects(
                [
                    Object(
                        uuid=uuid,
                        coords=Coords(x=x, y=y),
                        enemy_info=EnemyInfo(
                            health=health,
                            health_max=health_max,
                            name=name,
                            last_attack=last_attack,
                        ),
                    )
                ]
            )
        )

        users = server.game_state.get_local_users_distance(x, y)
        users = [u.uuid for u in users]

        if include_user_ids is not None:
            users = [u for u in users if u in include_user_ids]

        users_sessions = [
            server.game_state.user_sessions[u].peer
            for u in users
            if u in server.game_state.user_sessions
        ]

        if len(users_sessions) == 0:
            return

        await self.broadcast(r, include=users_sessions)

    async def give_damage(
        self, uuid: str, damage: int, include_user_ids: list[str] | None = None
    ) -> None:
        r = ServerMessage(give_damage=GiveDamage(damage=damage))

        users = server.game_state.users

        if include_user_ids is not None:
            users = [u for u in users if u in include_user_ids]

        users_sessions = [
            server.game_state.user_sessions[u].peer
            for u in users
            if u in server.game_state.user_sessions
        ]

        if len(users_sessions) == 0:
            return

        await self.broadcast(r, include=users_sessions)

    async def update_self(
        self,
        uuid: str,
    ) -> None:
        user = server.game_state.users[uuid]
        session = server.game_state.get_session(uuid)

        r = ServerMessage(users=Users(users=[user]))
        await server.game_state.update_remote_user(user)

        if session:
            await self.broadcast(r, include=[session])

    async def update_other_player_position(self) -> None:
        sessions = list(server.game_state.peer_sessions.values())

        for s in sessions:
            self_user = server.game_state.users.get(s.user_id, None)

            if self_user is None:
                continue

            users = await server.game_state.get_online_users_distance(
                self_user.coords.x, self_user.coords.y, s
            )

            new_known_users = set([u.uuid for u in users])
            old_known_users = s.known_users - new_known_users
            s.known_users = new_known_users

            for u in old_known_users:
                response = ServerMessage(logout=Logout(user=User(uuid=u)))
                await server.global_server.broadcast(response, include=[s.peer])

            message = ServerMessage(users=Users(users=users))

            await self.broadcast(message, include=[s.peer])
