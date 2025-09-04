#!/bin/python3
from hashlib import sha256
from Crypto.Util import number
from Crypto.Cipher import AES

BITS = 224

f = 26959946667150639794667015087019630673637144422540572481103610249993
g = 7

def reduce(a):
	while (l := a.bit_length()) > 224:
		a ^= f << (l - 225)
	return a

def mul(a,b):
	res = 0
	for i in range(b.bit_length()):
		if b & 1:
			res ^= a << i
		b >>= 1
	return reduce(res)

def pow(a,n):
	res = 1
	exp = a
	while n > 0:
		if n & 1:
			res = mul(res, exp)
		exp = mul(exp,exp)
		n >>= 1
	return res

if __name__ == '__main__':
	a = number.getRandomNBitInteger(BITS)
	A = pow(g,a)
	print(A)
	b = number.getRandomNBitInteger(BITS)
	B = pow(g,b)
	print(B)
	K = pow(A,b)
	assert K == pow(A,b)
	key = sha256(K.to_bytes(28)).digest()
	flag = open('../meta/flag.txt','r').read().encode()
	print(AES.new(key, AES.MODE_ECB).encrypt(flag + b'\x00' * (16 - len(flag) % 16)).hex())
