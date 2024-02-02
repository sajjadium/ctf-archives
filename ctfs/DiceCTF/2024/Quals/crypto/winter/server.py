#!/usr/local/bin/python

import os
from hashlib import sha256

class Wots:
	def __init__(self, sk, vk):
		self.sk = sk
		self.vk = vk

	@classmethod
	def keygen(cls):
		sk = [os.urandom(32) for _ in range(32)]
		vk = [cls.hash(x, 256) for x in sk]
		return cls(sk, vk)

	@classmethod
	def hash(cls, x, n):
		for _ in range(n):
			x = sha256(x).digest()
		return x

	def sign(self, msg):
		m = self.hash(msg, 1)
		sig = b''.join([self.hash(x, 256 - n) for x, n in zip(self.sk, m)])
		return sig

	def verify(self, msg, sig):
		chunks = [sig[i:i+32] for i in range(0, len(sig), 32)]
		m = self.hash(msg, 1)
		vk = [self.hash(x, n) for x, n in zip(chunks, m)]
		return self.vk == vk

if __name__ == '__main__':
	with open('flag.txt') as f:
		flag = f.read().strip()

	wots = Wots.keygen()

	msg1 = bytes.fromhex(input('give me a message (hex): '))
	sig1 = wots.sign(msg1)
	assert wots.verify(msg1, sig1)
	print('here is the signature (hex):', sig1.hex())

	msg2 = bytes.fromhex(input('give me a new message (hex): '))
	if msg1 == msg2:
		print('cheater!')
		exit()

	sig2 = bytes.fromhex(input('give me the signature (hex): '))
	if wots.verify(msg2, sig2):
		print(flag)
	else:
		print('nope')
