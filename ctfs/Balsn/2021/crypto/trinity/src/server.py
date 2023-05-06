#!/usr/local/bin/python3 -u
import signal
from blake3 import blake3


signal.alarm(15)

key = b'wikipedia.org/wiki/Trinity'.ljust(32)

God = bytes.fromhex(input('God >'))
GOd = bytes.fromhex(input('GOd >'))
GOD = bytes.fromhex(input('GOD >'))

trinity = {God, GOd, GOD}

assert 3 == len(trinity)
assert 1 == len({blake3(x, key=key).digest(8) for x in trinity})

with open('/flag.txt') as f:
    print(f.read())
