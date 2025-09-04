#!/usr/bin/env python3
import os
import sys
import hashlib

from ec import *
def bytes_to_long(a):
	return int(a.hex(),16)

#P-256 parameters
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
curve = EllipticCurve(p,a,b, order = n)
G = ECPoint(curve, 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

d_a = bytes_to_long(os.urandom(32))
P_a = G * d_a

def hash(msg):
	return int(hashlib.md5(msg).hexdigest(), 16)

def sign(msg : bytes, DEBUG = False):
	if type(msg) == str: msg = msg.encode()
	msg_hash = hash(msg)
	while True:
		k = bytes_to_long(os.urandom(n.bit_length() >> 3))
		R = G*k
		if R.inf: continue
		x,y = R.x, R.y
		r = x % n
		s = inverse(k, n) * (msg_hash + d_a) % n
		if r == 0 or s == 0: continue
		return r,s

def verify(r:int, s:int, msg:bytes, P_a):
	r %= n
	s %= n
	if r == 0 or s == 0: return False
	s1 = inverse(s,n)
	u = hash(msg) * s1 % n
	v = s1 % n
	R = G * u + P_a * v
	return r % n == R.x % n

def loop():
	while True:
		option = input('Choose an option:\n1 - get message/signature\n2 - get challenge to sign\n').strip()
		if option == '1':
			message = os.urandom(32)
			print(message.hex())
			signature = sign(message)
			assert(verify(*signature,message,P_a))
			print(signature)
		elif option == '2':
			challenge = os.urandom(32)
			signature = input(f'sign the following challenge {challenge.hex()}\n')
			r,s = [int(x) for x in signature.split(',')]
			if r == 0 or s == 0:
				print("nope")
			elif verify(r, s, challenge, P_a):
				print(open('flag.txt','r').read())
			else:
				print('wrong signature')
		else:
			print('Wrong input format')

if __name__ == '__main__':
	print('My public key is:')
	print(P_a)
	try:
		loop()
	except Exception as err:
		print(repr(err))
