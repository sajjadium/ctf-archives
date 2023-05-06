#!/usr/bin/env python3

from Crypto.Util.number import *
import string
from flag import flag

def randstr(l):
	rstr = [(string.printable[:62] + '_')[getRandomRange(0, 62)] for _ in range(l)]
	return ''.join(rstr)


def encrypt(msg, l):
	while True:
		rstr = 'CCTF{it_is_fake_flag_' + randstr(l) + '_90OD_luCk___!!}'
		p = bytes_to_long(rstr.encode('utf-8'))
		q = bytes_to_long(rstr[::-1].encode('utf-8'))
		if isPrime(p) and isPrime(q):
			n = p * q
			e, m = 65537, bytes_to_long(msg.encode('utf-8'))
			c = pow(m, e, n)
			return n, c

n, c = encrypt(flag, 27)

print(f'n = {n}')
print(f'c = {c}')