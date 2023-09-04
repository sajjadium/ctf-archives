#!/usr/bin/env python3

import os

def fnv1(s):
	h = 0xcbf29ce484222325
	for b in s:
		h *= 0x00000100000001b3
		h &= 0xffffffffffffffff
		h ^= b
	return h

TARGET = 0x1337133713371337

print("Welcome to FNV!")
print(f"Please enter a string in hex that hashes to 0x{TARGET:016x}:")
s = bytearray.fromhex(input())
if fnv1(s) == TARGET:
	print('Well done!')
	print(os.getenv('FLAG'))
else:
	print('Try again... :(')
