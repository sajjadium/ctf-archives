#!/usr/bin/env python3

from Crypto.Util.number import *
from random import *        
from os import urandom
from flag import flag

hubbub = 3

def mulvec(columns, vec):
	c = len(columns)
	assert(c == len(vec))
	r = len(columns[0])
	result = [0 for _ in range(r)]
	for i, bit in zip(range(c), vec):
		assert(len(columns[i]) == r)
		if bit == 1:
			for _ in range(r):
				result[_] ^= columns[i][_]
	return result

def barbyte(bar):
	l = len(bar)
	bar = ''.join([str(_) for _ in bar])
	bar = int(bar, 2)
	b = long_to_bytes(bar)
	while True:
		if len(b) < l // 8:
			b = b'\x00' + b
		else:
			break
	return b

def bytebar(bytes):
	i = bytes_to_long(bytes)
	vec = [int(_) for _ in bin(i)[2:].zfill(len(bytes) * 8)]
	return vec

class cognitivenc(object):

	@classmethod
	def new(cls, nbit = 48):
		key = cls.keygen(nbit)
		return cls(key)

	def __init__(self, key):
		self.key = key
		self.keylen = len(self.key)
		self.random = SystemRandom()

	@classmethod
	def keygen(cls, nbit):
		key = SystemRandom().getrandbits(nbit)
		key = bin(key)[2:].zfill(nbit)
		return [int(_) for _ in key]

	def encode(self, msg):
		l = len(msg)
		msg = bytes_to_long(msg)
		m = bin(msg)[2:].zfill(8 * l)
		m = [int(_) for _ in m]
		result = [0 for _ in range(self.keylen)]
		for i, b in enumerate(m):
			result[3*i + 0] = b
			result[3*i + 1] = b
			result[3*i + 2] = b
		return result

	def encrypt(self, msg):
		msg = self.encode(msg)
		l = len(msg)
		columns = []
		for _ in range(self.keylen):
			col = [int(_) for _ in bin(SystemRandom().getrandbits(self.keylen))[2:].zfill(self.keylen)]
			columns.append(col)

		y = mulvec(columns, self.key)
		y = [y[_] ^ msg[_] for _ in range(l)]

		for i in range(self.keylen // 3):
			idx = self.random.randrange(hubbub)
			y[3*i + idx] ^= 1

		columns = [barbyte(c) for c in columns]
		columns = b''.join(columns)
		return columns + barbyte(y)

def main():
	cipher = cognitivenc.new()
	random = SystemRandom()
	for _ in range(3117):
		pt = urandom(2)
		ct = cipher.encrypt(pt)
		fp = open("./output/ptext_{:04d}".format(_), "wb")
		fc = open("./output/ctext_{:04d}".format(_), "wb")
		fp.write(pt)
		fc.write(ct)
	enc = []

	for _ in range(len(flag) // 2):
		enc.append(cipher.encrypt(flag[_*2:_*2 + 2]))

	for _, ct in enumerate(enc):
		fe = open("./output/flag_{:02d}".format(_), "wb")
		fe.write(ct)

if len(flag) % 2 != 0: flag += b'+'

if __name__ == "__main__":
	main()