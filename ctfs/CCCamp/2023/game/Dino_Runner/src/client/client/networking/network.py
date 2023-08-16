import threading
import uuid
from asyncio import Lock, Queue, Task, create_task, iscoroutinefunction
from asyncio.exceptions import IncompleteReadError
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Tuple, TypeVar, cast

import aioprocessing
import betterproto

from client.game.state import GameState
from client.game.utils import check_wait, sleep
from shared.gen.messages.v1 import (
    AcknowledgeDamage,
    AttackEnemy,
    ClientMessage,
    Coords,
    Error,
    Interact,
    InteractStatus,
    LoggedIn,
    Login,
    Logout,
    MapChunkRequest,
    MapChunkResponse,
    ObjectAsset,
    ObjectAssetRequest,
    Objects,
    Ping,
    Runner,
    ServerMessage,
    ShopInteract,
    Users,
)
from shared.lazy import LazyDict
from shared.utils import AsyncLockEventHandler, EventHandler

ServerMessageType = TypeVar(
    "ServerMessageType",
    bound=ServerMessage.ping.__class__
    | ServerMessage.logged_in.__class__
    | ServerMessage.users.__class__
    | ServerMessage.chunk.__class__
    | ServerMessage.error.__class__
    | ServerMessage.logout.__class__
    | ServerMessage.objects.__class__
    | ServerMessage.object_asset.__class__
    | ServerMessage.interact.__class__
    | ServerMessage.give_damage.__class__,
)


AyncMessageHandlerType = Callable[[ServerMessageType, Lock], Awaitable[None]]
MessageHandlerType = Callable[[ServerMessageType], None]
ErrorHandlerType = Callable[[Error], None]


class Connection:
    runner_con: aioprocessing.AioQueue  # type: ignore
    thread_con: aioprocessing.AioQueue  # type: ignore
    connected: bool = False
    error_handler: ErrorHandlerType
    # (ClientMessage, (Handler, ErrorHandler)) If ErrorHandler None, the default error Handler is used
    network_queue: Queue[
        Tuple[
            ClientMessage,
            Tuple[
                MessageHandlerType[...] | AyncMessageHandlerType[...] | None,
                ErrorHandlerType | None,
            ],
        ]
    ]
    handlers: Dict[
        str,
        Tuple[
            MessageHandlerType[...] | AyncMessageHandlerType[...] | None,
            ErrorHandlerType | None,
        ],
    ]
    game_state: GameState
    start_connection_lock: Lock
    task_list: set[Task[None]]

    def __init__(
        self,
        runner_con: aioprocessing.AioQueue,  # type: ignore
        thread_con: aioprocessing.AioQueue,  # type: ignore
        error_handler: ErrorHandlerType,
        game_state: GameState,
    ) -> None:
        self.runner_con = runner_con
        self.thread_con = thread_con
        self.error_handler = error_handler
        self.network_queue = Queue()
        self.handlers = {}
        self.game_state = game_state
        self.start_connection_lock = Lock()
        self.task_list = set()

        self.ping_handler = EventHandler()
        self.users_handler = EventHandler()
        self.logout_handler = EventHandler()
        self.objects_handler = EventHandler()
        self.login_handler = EventHandler()
        self.interact_handler = EventHandler()
        self.map_chunk_handler = AsyncLockEventHandler()

    async def ping_loop(self, running: threading.Event) -> None:
        while running.is_set():
            if self.game_state.is_authenticated():
                await self.ping()

            # await sleep(1)
            for _ in range(100):
                await sleep(1 / 100)

    async def read_message_loop(self, running: threading.Event) -> None:
        while running.is_set():
            await check_wait()

            try:
                d: dict[str, Any] = cast(
                    dict[str, Any], await self.runner_con.coro_get()
                )
                message: LazyDict = LazyDict(d, ServerMessage)

                message_id = message.uuid
                match message:
                    case {"ping": inner_message}:
                        self.ping_handler(LazyDict(inner_message, Ping))
                    case {"loggedIn": inner_message}:
                        self.login_handler(LazyDict(inner_message, LoggedIn))
                    case {"error": inner_message}:
                        error = LazyDict(inner_message, Error)
                        # logging.error(f"{ErrorType(error.type).name} {error.message}")
                    case {"users": inner_message}:
                        self.users_handler(LazyDict(inner_message, Users))
                    case {"logout": inner_message}:
                        self.logout_handler(LazyDict(inner_message, Logout))
                    case {"objects": inner_message}:
                        self.objects_handler(LazyDict(inner_message, Objects))
                    case {"interact": inner_message}:
                        self.interact_handler(LazyDict(inner_message, Interact))
                    case {"chunk": inner_message}:
                        task = create_task(
                            self.map_chunk_handler(
                                LazyDict(inner_message, MapChunkResponse)
                            ),
                            name="chunk",
                        )
                        self.task_list.add(task)
                        task.add_done_callback(self.task_list.discard)
                    case {"giveDamage": inner_message}:
                        self.acknowledge_damage(damage=inner_message["damage"])
                    case _:
                        pass

                handler = None
                error_handler = None
                if message_id in self.handlers:
                    handler, error_handler = self.handlers[message_id]
                    del self.handlers[message_id]

                match message:
                    case {"error": inner_message}:
                        error = LazyDict(inner_message, Error)
                        if error_handler is None:
                            self.error_handler(cast(Error, error))
                        else:
                            error_handler(cast(Error, error))
                    case {"uuid": _, **inner_message}:
                        if handler is not None:
                            key, value = next(inner_message.items().__iter__())
                            key = betterproto.casing.safe_snake_case(key)

                            sub_cls = ServerMessage._cls_for(ServerMessage.__dataclass_fields__[key])  # type: ignore
                            x = LazyDict(value, sub_cls)

                            if iscoroutinefunction(handler):
                                task = create_task(handler(x), name=key)
                                self.task_list.add(task)
                                task.add_done_callback(self.task_list.discard)
                            else:
                                handler(x)  # type: ignore
                    case _:
                        print("MEH")

            except (IncompleteReadError, BrokenPipeError):
                await sleep(0.1)

    async def send_message_loop(self, running: threading.Event) -> None:
        while running.is_set():
            message, handler = await self.network_queue.get()
            message_id = str(uuid.uuid4())

            message.uuid = message_id
            self.handlers[message_id] = handler

            self.thread_con.put(message.to_dict())

    async def ping(
        self,
        handler: MessageHandlerType[Ping] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ) -> None:
        ping = ClientMessage(ping=Ping(time=datetime.now()))

        await self.network_queue.put((ping, (handler, error_handler)))

    def login(
        self,
        username: str,
        password: str,
        handler: MessageHandlerType[LoggedIn] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ) -> None:
        login = ClientMessage(login=Login(username=username, password=password))

        self.network_queue.put_nowait((login, (handler, error_handler)))

    def move(
        self,
        x: float,
        y: float,
        rotation: float,
        error_handler: ErrorHandlerType | None = None,
    ) -> None:
        coords = ClientMessage(coords=Coords(x=x, y=y, rotation=rotation))

        self.network_queue.put_nowait((coords, (None, error_handler)))

    def get_chunks(
        self,
        x: int,
        y: int,
        handler: AyncMessageHandlerType[MapChunkResponse] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ) -> None:
        get_chunk_msg = ClientMessage(chunk_request=MapChunkRequest(x=int(x), y=int(y)))

        self.network_queue.put_nowait((get_chunk_msg, (handler, error_handler)))

    def get_object_asset(
        self,
        uuid: str,
        handler: MessageHandlerType[ObjectAsset] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ) -> None:
        get_object_asset = ClientMessage(
            object_asset_request=ObjectAssetRequest(uuid=uuid)
        )

        self.network_queue.put_nowait((get_object_asset, (handler, error_handler)))

    def interact(
        self,
        uuid: str,
        status: InteractStatus,
        text: str = "",
        shop: list[ShopInteract] = [],
        runner: Runner | None = None,
        handler: MessageHandlerType[Interact] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ) -> None:
        interact = ClientMessage(
            interact=Interact(
                uuid=uuid,
                text=text,
                status=status,
                shop=shop,
                runner=runner if runner is not None else Runner(),
            )
        )

        self.network_queue.put_nowait((interact, (handler, error_handler)))

    def acknowledge_damage(
        self,
        damage: int,
        handler: MessageHandlerType[Interact] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ):
        acknowledge_damage = ClientMessage(acknowledge_damage=AcknowledgeDamage(damage))

        self.network_queue.put_nowait((acknowledge_damage, (handler, error_handler)))

    def attack_enemy(
        self,
        time: datetime,
        uuid: str,
        damage: int,
        handler: MessageHandlerType[Interact] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ):
        attack_enemy_msg = ClientMessage(
            attack_enemy=AttackEnemy(time=time, uuid=uuid, damage=damage)
        )

        self.network_queue.put_nowait((attack_enemy_msg, (handler, error_handler)))

    def logout(
        self,
        handler: MessageHandlerType[Interact] | None = None,
        error_handler: ErrorHandlerType | None = None,
    ) -> None:
        logout = ClientMessage(logout=Logout())

        self.network_queue.put_nowait((logout, (handler, error_handler)))
