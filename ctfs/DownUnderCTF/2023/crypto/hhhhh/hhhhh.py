#!/usr/bin/env python3
from os import getenv as hhhhhhh
from hashlib import md5 as hhhhh

def hhhhhh(hhh):
    h = hhhhh()
    hh = bytes([0] * 16)
    for hhhh in hhh:
        h.update(bytes([hhhh]))
        hh = bytes([hhhhhhh ^ hhhhhhhh for hhhhhhh, hhhhhhhh in zip(hh, h.digest())])
    return hh

print('hhh hhh hhhh hhh hhhhh hhhh hhhh hhhhh hhhh hh hhhhhh hhhh?')

h = bytes.fromhex(input('h: '))

if hhhhhh(h) == b'hhhhhhhhhhhhhhhh':
    print('hhhh hhhh, hhhh hh hhhh hhhh:', hhhhhhh('FLAG'))
else:
    print('hhhhh, hhh hhhhh!')
