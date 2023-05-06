from os import urandom
from lib51 import LFSR
from secret import msg, alex, tom

key = list(urandom(8))
iv  = int.from_bytes(urandom(2), 'little') % 4096
strm = LFSR(key, iv)

y = 0
for i in range(len(msg) * 8):
    y <<= 1
    y |= strm.getbit()

print(f"enc -> {int(msg.hex(), 16) ^ y :0x}")