#!/usr/bin/env python3

from Crypto.Util.number import *
from gensafeprime import *
from flag import flag

def keygen(nbit):
	p, q = [generate(nbit) for _ in range(2)]
	return (p, q)

def encrypt(m, pubkey):
	return pow(pubkey + 1, m, pubkey ** 3)

p, q = keygen(512)
n = p * q

flag = bytes_to_long(flag)
enc = encrypt(flag, n)

print(f'pubkey = {n}')
print(f'enc = {enc}')