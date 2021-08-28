#!/usr/bin/env python3
import os

def splitit(n):
	return (n >> 4), (n & 0xF)

def encrypt(n, key1, key2):
	m, l = splitit(n)
	e = ((m ^ key1) << 4) | (l ^ key2)
	return e

FLAG = open('flag.txt').read().lstrip('wormcon{').rstrip('}')
alpha = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

assert all(x in alpha for x in FLAG)

otp = int(os.urandom(1).hex(), 16)
otpm, otpl = splitit(otp)

print(f"{otp = }")
cipher = []

for i,ch in enumerate(FLAG):
	if i % 2 == 0:
		enc = encrypt(ord(ch), otpm, otpl)
	else:
		enc = encrypt(ord(ch), otpl, otpm)
	cipher.append(enc)

cipher = bytes(cipher).hex()
print(f'{cipher = }')

open('out.txt','w').write(f'cipher = {cipher}')