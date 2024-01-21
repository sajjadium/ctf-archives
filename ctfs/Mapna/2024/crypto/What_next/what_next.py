#!/usr/bin/env python3

from random import *
from Crypto.Util.number import *
from flag import flag

def encrypt(msg, KEY):
	m = bytes_to_long(msg)
	c = KEY ^ m
	return c

n = 80
TMP = [getrandbits(256) * _ ** 2 for _ in range(n)]
KEY = sum([getrandbits(256 >> _) for _ in range(8)]) 

enc = encrypt(flag, KEY)

print(f'TMP = {TMP}')
print(f'KEY = {KEY}')
print(f'enc = {enc}')