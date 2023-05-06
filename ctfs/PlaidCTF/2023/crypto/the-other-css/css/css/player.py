import asyncio
from secrets import token_bytes

from .cipher import Cipher
from .io_manager import ReaderWriter
from .keys import authentication_key
from .keys import player_key as player_key_data
from .mangle import mangle, unmangle
from .mode import Mode


class Player:
	disk: str

	def __init__(self, disk: str):
		self.disk = disk

	async def _read_or_fail(self, rw: ReaderWriter, size: int) -> bytes:
		data = await rw.read(size)
		if len(data) != size:
			raise Exception("Unexpected EOF")
		return data

	async def _write(self, rw: ReaderWriter, data: bytes) -> None:
		await rw.write(data)

	async def start(self, rw: ReaderWriter) -> None:
		# host issues player 16-byte challenge
		host_challenge = await self._read_or_fail(rw, 16)
		challenge_key = host_challenge[:8]
		encrypted_host_nonce = host_challenge[8:]
		cipher = Cipher(authentication_key, Mode.Authentication)
		host_mangling_key = cipher.encrypt(challenge_key)
		response = mangle(host_mangling_key, encrypted_host_nonce)
		await self._write(rw, response)

		cipher = Cipher(authentication_key, Mode.Authentication)
		host_nonce = cipher.decrypt(encrypted_host_nonce)

		# player issues host 16-byte challenge
		player_challenge_key = token_bytes(8)
		player_nonce = token_bytes(8)
		cipher = Cipher(authentication_key, Mode.Authentication)
		encrypted_player_nonce = cipher.encrypt(player_nonce)
		await self._write(rw, player_challenge_key + encrypted_player_nonce)

		cipher = Cipher(authentication_key, Mode.Authentication)
		player_mangling_key = cipher.encrypt(player_challenge_key)
		response = await self._read_or_fail(rw, 8)
		cipher = Cipher(authentication_key, Mode.Authentication)
		if cipher.decrypt(unmangle(player_mangling_key, response)) != player_nonce:
			await rw.write_eof()
			raise Exception("Authentication failed")

		# compute session key
		mangling_key = bytes(a ^ b for a, b in zip(host_mangling_key, player_mangling_key))
		session_nonce = bytes(a ^ b for a, b in zip(host_nonce, player_nonce))
		session_key = mangle(mangling_key, session_nonce)

		with open(self.disk, "rb") as f:
			# get disk key
			player_key_id, player_key = player_key_data
			f.seek(8 * player_key_id)
			encrypted_disk_key = f.read(8)
			cipher = Cipher(player_key, Mode.DiskKey)
			disk_key = cipher.decrypt(encrypted_disk_key)

			# read and send data to the host
			stream_cipher = Cipher(session_key, Mode.Data)
			f.seek(8 * 128)
			sector_index = 0
			while True:
				sector_nonce = f.read(8)
				if len(sector_nonce) == 0:
					break
				sector_key = mangle(disk_key, sector_nonce)
				sector_cipher = Cipher(sector_key, Mode.Data)
				data = sector_cipher.decrypt(f.read(8208))
				await self._write(rw, stream_cipher.encrypt(data))
				sector_index += 1
				await asyncio.sleep(0) # yield to other tasks
			await rw.write_eof()
