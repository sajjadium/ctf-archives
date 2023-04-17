from itertools import count, cycle
from secrets import token_bytes
from sys import argv

from .cipher import Cipher
from .mangle import mangle
from .mode import Mode

sector_size = 8192

assert len(argv) == 4, "usage: make_disk.py <output-file> <input-file> <disk-keys-file>"

with open(argv[1], "wb") as f:
	disk_key = token_bytes(8)

	with open(argv[3], "rb") as g:
		for i in range(128):
			player_key = g.read(8)
			assert len(player_key) == 8
			cipher = Cipher(player_key, Mode.DiskKey)
			f.write(cipher.encrypt(disk_key))

	with open(argv[2], "rb") as g:
		for i in count():
			print(f"sector {i}")
			sector = g.read(sector_size)

			if len(sector) == 0:
				break

			sector_nonce = token_bytes(8)
			sector_key = mangle(disk_key, sector_nonce)
			sector_xor = token_bytes(16)
			f.write(sector_nonce)
			cipher = Cipher(sector_key, Mode.Data)
			f.write(cipher.encrypt(sector_xor))
			sector_xord = bytes(a ^ b for a, b in zip(sector, cycle(sector_xor)))
			f.write(cipher.encrypt(sector_xord))

