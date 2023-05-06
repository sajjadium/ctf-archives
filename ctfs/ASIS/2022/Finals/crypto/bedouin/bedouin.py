#!/usr/bin/env python3

from Crypto.Util.number import *
from secret import nbit, l, flag

def genbed(nbit, l):
	while True:
		zo = bin(getPrime(nbit))[2:]
		OZ = zo * l + '1'
		if isPrime(int(OZ)):
			return int(OZ)

p, q = [genbed(nbit, l) for _ in '01']
n = p * q
d = 1 ^ l ** nbit << 3 ** 3
phi = (p - 1) * (q - 1)
e = inverse(d, phi)
m = bytes_to_long(flag)
c = pow(m, e, n)

if pow(c, d, n) == m:
	print(f'n = {n}')
	print(f'c = {c}')