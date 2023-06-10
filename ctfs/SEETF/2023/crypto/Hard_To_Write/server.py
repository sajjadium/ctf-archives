from server_secrets import FLAG # only server has this!
import re
import os
import sys

import numpy as np
from cipher import byte2int, encrypt

m = re.match(r"^SEE\{(.+)\}$", FLAG)
assert m
naked_flag = m.groups()[0].encode()

key = byte2int(np.frombuffer(os.urandom(8), dtype=np.uint8))
print("Encrypted flag:", encrypt(naked_flag, key).hex(), flush=True)

print("Hex encoded buffer:", flush=True)
try: toencrypt = bytes.fromhex(sys.stdin.readline().strip())
except: raise Exception("uwu")

assert len(toencrypt) <= 10000000
assert len(toencrypt) % 8 == 0

encrypted = encrypt(toencrypt, key)
print("Encrypted:", flush=True)
print(encrypted.hex(), flush=True)