from asyncio.queues import Queue
from os import getenv
from sys import stdout
from typing import Optional

from hexdump import hexdump


class IOManager:
	name: str
	color: str
	closed: bool
	queue: Queue[Optional[bytes]]
	buffer: bytes

	def __init__(self, name: str, color: Optional[str] = None):
		self.name = name
		self.color = color if color is not None else ""
		self.closed = False
		self.queue = Queue()
		self.buffer = b""

	async def write(self, data: bytes) -> None:
		if getenv("DEBUG") == "1":
			print(f"{self.color}[{self.name}] writing {len(data)} bytes")
			hexdump(data)
			stdout.write("\x1b[0m")
			stdout.flush()
		await self.queue.put(data)

	async def read(self, size: int) -> bytes:
		if self.closed:
			raise Exception("Unexpected EOF")
		while len(self.buffer) < size:
			chunk = await self.queue.get()
			if chunk is None:
				self.closed = True
				break
			self.buffer += chunk
		if len(self.buffer) < size:
			raise Exception("Unexpected EOF")
		data = self.buffer[:size]
		self.buffer = self.buffer[size:]
		return data

	async def read_eof(self) -> bytes:
		while not self.closed:
			chunk = await self.queue.get()
			if chunk is None:
				self.closed = True
				break
			self.buffer += chunk
		return self.buffer

class ReaderWriter:
	reader: IOManager
	writer: IOManager

	def __init__(self, reader: IOManager, writer: IOManager):
		self.reader = reader
		self.writer = writer

	async def read(self, size: int) -> bytes:
		return await self.reader.read(size)

	async def write(self, data: bytes) -> None:
		await self.writer.write(data)

	async def write_eof(self) -> None:
		await self.writer.queue.put(None)
