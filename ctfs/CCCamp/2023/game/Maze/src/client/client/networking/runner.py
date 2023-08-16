import logging
import struct
from asyncio import (
    IncompleteReadError,
    Lock,
    StreamReader,
    StreamWriter,
    open_connection,
)
from multiprocessing.synchronize import Event as EventClass
from typing import Any, cast

import aioprocessing

from client.game.utils import sleep
from shared.gen.messages.v1 import ClientMessage, ServerMessage


class Runner:
    host: str
    port: int
    ssl: bool
    reader: StreamReader
    writer: StreamWriter
    start_connection_lock: Lock
    connected: bool

    runner_con: aioprocessing.AioQueue  # type: ignore
    thread_con: aioprocessing.AioQueue  # type: ignore

    def __init__(
        self,
        runner_con: aioprocessing.AioQueue,  # type: ignore
        thread_con: aioprocessing.AioQueue,  # type: ignore
        host: str,
        port: int,
        ssl: bool,
    ) -> None:
        self.runner_con = runner_con
        self.thread_con = thread_con
        self.host = host
        self.port = port
        self.ssl = ssl
        self.start_connection_lock = Lock()

        self.connected = False

    async def read_message_loop(self, running: EventClass) -> None:
        await self._start_connection()

        while running.is_set():
            try:
                size_buf = await self.reader.readexactly(4)

                size = struct.unpack("!i", size_buf)[0]
                data_buf = await self.reader.readexactly(size)

                message = ServerMessage().parse(data_buf)
                self.runner_con.put(message.to_pydict())
            except (IncompleteReadError, BrokenPipeError):
                await sleep(0.1)

    async def send_message_loop(self, running: EventClass) -> None:
        await self._start_connection()

        while running.is_set():
            message_dict = cast(dict[str, Any], await self.thread_con.coro_get())

            message: ClientMessage = ClientMessage().from_dict(message_dict)
            packet = message.SerializeToString()

            await self._send_message(client_message=packet)

    async def _start_connection(self) -> None:
        async with self.start_connection_lock:
            if not self.connected or self.writer.is_closing():
                sucess = False
                while not sucess:
                    try:
                        self.reader, self.writer = await open_connection(
                            host=self.host,
                            port=self.port,
                            ssl=self.ssl,
                        )
                        sucess = True
                        self.connected = True

                        logging.debug("New Connection")
                    except Exception:
                        logging.debug("Error establishing connection")
                        await sleep(delay=0.1)

    async def _send_message(self, client_message: bytes) -> None:
        await self._start_connection()

        message = struct.pack("!i", len(client_message)) + client_message

        self.writer.write(message)
