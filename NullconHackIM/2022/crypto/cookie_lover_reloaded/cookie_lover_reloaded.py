#!/usr/bin/env python3
import os
import sys
import hashlib

from ec import *
from secret import flag

#P-256 parameters
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
curve = EllipticCurve(p,a,b, order = n)
G = ECPoint(curve, 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

target = b'I still love cookies.'
d_a = bytes_to_long(os.urandom(32))
P_a = G * d_a

def sign(msg : bytes, DEBUG = False):
	if type(msg) == str: msg = msg.encode()
	if not DEBUG:
		#I will not talk about cookies.
		if b'cookie' in msg:
			return 0,0
		#no control characters allowed in message
		if any([c < 32 for c in msg]):
			return 0,0
	#regular message
	k = int(hashlib.md5(os.urandom(16)).hexdigest()[:4], 16)
	R = G*k
	x,y = R.x, R.y
	r = x % n
	s = inverse(k, n) * (int(hashlib.md5(msg).hexdigest(),16) + r * d_a) % n
	return r,s

def verify(r:int, s:int, msg:bytes, P_a):
	s1 = inverse(s,n)
	u = int(hashlib.md5(msg).hexdigest(), 16) * s1 % n
	v = r * s1 % n
	R = G * u + P_a * v
	return r % n == R.x % n

def loop():
	print('I will sign anythin as long as it does not talk about cookies.')
	while True:
		print('Choose an option:\n1:[text to sign]\n2:[number,number - signature to check]\n')
		sys.stdout.flush()
		cmd = sys.stdin.buffer.readline().strip()
		if cmd[:2] == b'1:':
			print(sign(cmd[2:]))
		elif cmd[:2] == b'2:':
			r,s = [int(x) for x in cmd[2:].decode().split(',')]
			if verify(r, s, target, P_a):
				print(flag)
			else:
				print('wrong signature')
		else:
			print('Wrong input format')

if __name__ == '__main__':
	r,s = sign(target, True)
	assert verify(r,s,target,P_a)
	print('My public key is:')
	print(P_a)
	try:
		loop()
	except Exception as err:
		print(repr(err))
