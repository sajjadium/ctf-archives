#!/usr/bin/env python3

from Crypto.Util.number import *
import random
import os

class LFSR():

	def __init__(self, taps):

		d = max(taps)
		self.taps = [d-t for t in taps]
		self.state = [random.randint(0, 1) for _ in range(d)]

	def _sum(self, L):

		res = 0
		for t in L:
			res ^= t
		return res

	def next(self):

		s = self.state[0]
		self.state = self.state[1:] + [self._sum([self.state[t] for t in self.taps])]
		return s

	def getPrime(self, nbits):

		count = 0
		while True:
			count += 1
			p = int("".join([str(self.next()) for _ in range(nbits)]), 2)
			if isPrime(p) and p > 2**(nbits-1):
				print(f"[LOG] It takes {count} trials to find a prime.")
				return p

if __name__ == '__main__':

	lfsr = LFSR([47, 43, 41, 37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2])
	p, q = lfsr.getPrime(512), lfsr.getPrime(512)
	with open("flag.txt", "rb") as f:
		flag = f.read()
	print(f"n = {p*q}")
	print(f"enc = {pow(bytes_to_long(flag), 0x10001, p*q)}")
