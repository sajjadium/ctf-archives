#!/usr/local/bin/python3.8

from os import urandom
from Crypto.Util.number import inverse
from hashlib import sha256
from Crypto.Random import random
import ecdsa
from flag import FLAG

class PRNG:
	def __init__(self,seed,m,flag):
		self.state = seed
		self.m = m
		self.counter = 0
		self.flag = flag

	def next_state(self):	
			b = self.flag[self.counter % len(self.flag)]
			self.state = (self.state + b) % self.m
			self.counter += 1
			return self.state


C = ecdsa.NIST256p
G = C.generator
N = int(C.order)

seed = random.randint(1,N-1)

prng = PRNG(seed,N,FLAG)

private_key = int(sha256(urandom(16)).hexdigest(),16) % N

public_key = G * private_key

print("Public key : ",(int(public_key.x()),int(public_key.y())))

signatures = []

for i in range(len(FLAG)):
	k = prng.next_state() % N
	P = G * k
	r = int(P.x()) % N
	h = int(sha256(urandom(16)).hexdigest(),16)
	s = inverse(k,N)*(h+r*private_key)%N
	signatures.append([h,r,s])

print(signatures)