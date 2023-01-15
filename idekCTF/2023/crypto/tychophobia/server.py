#!/usr/bin/env python3

from Crypto.Util.number import *
import random
import os
import signal

class FeisteLCG():

	def __init__(self, k, seed):

		self.k = k

		self.m = 2**(2*k)
		self.a = getPrime(k)
		self.x = seed
		self.b = 0

		print(f"a = {self.a}")
		print(f"b = {self.b}")

		# Generate random permutation by swapping
		self.p = list(range(k))
		for i in range(k-1):
			j = i + random.randint(0, k-i-1)
			self.p[i], self.p[j] = self.p[j], self.p[i]
		
		# Start with identity
		self.key = list(range(k))
	
	def next(self):

		self.x = (self.a * self.x + self.b) % self.m
		
		# Split the state into left and right 
		left, right = self.x >> self.k, self.x % 2**self.k

		# 13-round Alternating Feistel scheme
		for _ in range(13):
			left, right = right, left ^ self.perm_bits(right, self.key)
			left, right = right, left ^ self.perm_bits(right, self.key)

		# Update the key
		self.key = self.perm(self.key, self.p)

		# I'm evil and only give you upper bits :D
		return left

	def perm(self, L, key):

		return [L[key[i]] for i in range(self.k)]

	def perm_bits(self, n, key):

		bits = list(bin(n)[2:].zfill(self.k))
		return int("".join(self.perm(bits, self.key)), 2)

def Challenge():

	print("========================")
	print("=== Mission Possible ===")
	print("========================")
	print("")

	print("I'll give you 2023 consecutive outputs of the RNG,") 
	print("you just need to recover the seed. Sounds easy, right?")
	print("")

	seed = bytes_to_long(os.urandom(16))
	rng = FeisteLCG(64, seed)

	for _ in range(2023):
		print(rng.next())
	print("")

	inp = int(input("Guess the seed: "))
	if inp == seed:
		with open("flag.txt", "r") as f:
			print(f.read())
	else:
		print("Nope :<")

if __name__ == '__main__':

	signal.alarm(1200)
	Challenge()
    
