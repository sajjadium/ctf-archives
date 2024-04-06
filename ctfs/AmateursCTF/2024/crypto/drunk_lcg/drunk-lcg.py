#!/usr/local/bin/python3

import sys
from random import randint
from Crypto.Util.number import *

m = 150094635296999121
flag = bytes_to_long(open('flag.txt', 'rb').read())
upper = 1 << (flag.bit_length() + 1)
bl = upper.bit_length()//4

def print(a):
    sys.stdout.write(hex(a)[2:].zfill(bl))
    sys.stdout.write('\n')

def lcg():
    a = randint(0, m)
    c = randint(0, m)
    seed = randint(0, m)
    while True:
        seed = (a * seed + c) % m
        yield seed

def randbelow(n):
    a = next(x)
    while a < n:
        a *= m
        a += next(x)
    return a % n

def trial():
    global x
    x = iter(lcg())
    print(flag ^ randbelow(upper))
    print(flag ^ randbelow(upper))

trial()
sys.stdout.flush()