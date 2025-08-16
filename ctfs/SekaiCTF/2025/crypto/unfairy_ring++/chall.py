from functools import reduce
from uov import uov_1p_pkc as uov # https://github.com/mjosaarinen/uov-py/blob/main/uov.py
import os
FLAG = os.getenv("FLAG", "SEKAI{TESTFLAG}")

def xor(a, b):
    assert len(a) == len(b), "XOR inputs must be of the same length"
    return bytes(x ^ y for x, y in zip(a, b))

names = ['Miku', 'Ichika', 'Minori', 'Kohane', 'Tsukasa', 'Kanade']
pks = [uov.expand_pk(uov.shake256(name.encode(), 43576)) for name in names]
msg = b'SEKAI'

sig = bytes.fromhex(input('Ring signature (hex): '))
assert len(sig) == 112 * len(names), 'Incorrect signature length'

t = reduce(xor, [uov.pubmap(sig[i*112:(i+1)*112], pks[i]) for i in range(len(names))])
assert t == uov.shake256(msg, 44), 'Invalid signature'

print(FLAG)