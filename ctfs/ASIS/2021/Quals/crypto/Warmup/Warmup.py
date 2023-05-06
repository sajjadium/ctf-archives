#!/usr/bin/env python3

from Crypto.Util.number import *
import string
from secret import is_valid, flag

def random_str(l):
	rstr = ''
	for _ in range(l):
		rstr += string.printable[:94][getRandomRange(0, 93)]
	return rstr

def encrypt(msg, nbit):
	l, p = len(msg), getPrime(nbit)
	rstr = random_str(p - l)
	msg += rstr
	while True:
		s = getRandomNBitInteger(1024)
		if is_valid(s, p):
			break
	enc = msg[0]
	for i in range(p-1):
		enc += msg[pow(s, i, p)]
	return enc

nbit = 15
enc = encrypt(flag, nbit)
print(f'enc = {enc}')