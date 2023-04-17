import asyncio
from sys import stdin, stdout

from .io_manager import IOManager, ReaderWriter
from .player import Player


async def main():
	player = Player("../disks/a.disk")

	host_to_player = IOManager("host -> player", color = "\x1b[31m")
	player_to_host = IOManager("player -> host", color = "\x1b[34m")

	player_task = player.start(ReaderWriter(host_to_player, player_to_host))
	stdin_task = stdin_to_manager(host_to_player)
	stdout_task = manager_to_stdout(player_to_host)

	await asyncio.gather(player_task, stdin_task, stdout_task)

async def stdin_to_manager(manager: IOManager):
	loop = asyncio.get_running_loop()
	reader = asyncio.StreamReader()
	protocol = asyncio.StreamReaderProtocol(reader)
	await loop.connect_read_pipe(lambda: protocol, stdin)

	while True:
		data = await reader.read(1024)
		if len(data) == 0:
			break
		await manager.write(data)
	await manager.queue.put(None)

async def manager_to_stdout(manager: IOManager):
	while True:
		chunk = await manager.queue.get()
		if chunk is None:
			break
		stdout.buffer.write(chunk)
		stdout.flush()

if __name__ == "__main__":
	asyncio.run(main())
