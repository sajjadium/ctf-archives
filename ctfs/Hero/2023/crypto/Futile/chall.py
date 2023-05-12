#!/usr/bin/env python
from pylfsr import LFSR
from functools import reduce
import os

flag = os.environ.get('FLAG','Hero{fake_flag}').encode()

def binl2int(l: list) -> int:
    return reduce(lambda x,y: 2*x+y, l)

def lfsr() -> LFSR:
    return LFSR(fpoly=[8,6,5,4], initstate='random')

def get_uint8() -> int:
    return binl2int(lfsr().runKCycle(8))

def mask(flag: bytes) -> str:
    return bytearray(f ^ get_uint8() for f in flag).hex()

while True:
    try:
        input('Hero{' + mask(flag[5:-1]) + '}\n')
    except:
        pass
