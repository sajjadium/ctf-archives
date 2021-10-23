#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import FLAG

def gentuple(nbit):
	a, b, c = [getPrime(nbit // 3) for _ in '012']
	return a, b, c

def encrypt(msg, params):
	a, b, c = params
	e, n = 65537, a * b * c
	m = bytes_to_long(msg)
	assert m < n
	enc = pow(m, e, n)
	return enc

nbit = 513
a, b, c = gentuple(nbit)
enc = encrypt(FLAG, (a, b, c))

print(f'a*b + c = {a*b + c}')
print(f'b*c + a = {b*c + a}')
print(f'c*a + b = {c*a + b}')
print(f'enc % a = {enc % a}')
print(f'enc % b = {enc % b}')
print(f'enc % c = {enc % c}')
print(f'enc     = {enc}')