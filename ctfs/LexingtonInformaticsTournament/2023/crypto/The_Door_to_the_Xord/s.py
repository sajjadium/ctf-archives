#!/usr/bin/env python3
import random
from Crypto.Util.number import long_to_bytes as ltb, bytes_to_long as btl

with open("flag.txt", "rb") as f:
	x = f.read().strip()

assert len(x) == 32

def xor(x, y):
	# the better way to xor strings
	# (just in case they have different length, one will be treated as if it was rjusted with \0s)
	return ltb(btl(x)^btl(y))

while True:
	input("Press enter to get some gibberish: ")
	blen = len(x)*8

	val = random.getrandbits(blen)
	print(xor(x, ltb(val)).hex())