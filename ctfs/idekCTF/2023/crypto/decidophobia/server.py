#!/usr/bin/env python3

from Crypto.Util.number import *
import random
import signal

class Pool():

	def __init__(self):

		self.p, self.q, self.r = None, None, None

class PrimeMan():

	def __init__(self):

		self.p, self.q, self.r = None, None, None

	def gen(self, nbits, ticket):

		self.p = getPrime(nbits)
		self.q = getPrime(nbits)
		self.r = getPrime(nbits)

		self.n = self.p * self.q * self.r

		self.enc = pow(ticket, 0x10001, self.n)

		print("You: Integer factoring is hard! No one can steal my ticket now :D.")

	def throw_primes(self, pool):

		print("Today, you go to the forest to cut down trees as usual. You see a good tree to cut down. The tree is near a pool. But you already worked hard all day. You could not hold your ax and primes very well. The primes slip out of your hands. They go in to the pool.")

		pool.p, pool.q, pool.r = self.p, self.q, self.r
		self.p, self.q, self.r = None, None, None

	def print_backpack(self):

		print("")
		print(f"n = {self.n}")
		print(f"enc = {self.enc}")

class Mercury():

	def __init__(self):

		self.p, self.q, self.r = None, None, None

	def welcome_msg(self):

		print("")
		print("Mercury: What happened? Why are you crying?")

		print("")
		print("[1] I lost my primes in the pool. It is the only thing I have, I cannot recover the key without it.")
		print("[2] Ignore Mercury")

		op = int(input(">>> "))
		if op == 2:
			print("")
			print("No, you cannot ignore me <3.")

	def find_primes(self, pool):

		print("")
		print("Mercury jumps into the pool ... ")
		self.p, self.q, self.r = pool.p, pool.q, pool.r
		pool.p, pool.q, pool.r = None, None, None
		print("He comes up with a good prime, a silver prime and a bronze prime!")

	def oblivious(self):

		P = getPrime(384)
		Q = getPrime(384)

		N = P * Q
		d = pow(0x10001, -1, (P-1)*(Q-1))

		x1 = random.randint(0, N-1)
		x2 = random.randint(0, N-1)
		x3 = random.randint(0, N-1)

		print("Mercury: It's boring to directly give you prime back, I'll give you the prime thrugh oblivious transfer! Here are the parameters: ")
		print("")
		print(f"N = {N}")
		print(f"x1 = {x1}")
		print(f"x2 = {x2}")
		print(f"x3 = {x3}")

		"""
			Pick a random r and compute v = r**65537 + x1/x2/x3
			If you added x1/x2/x3, then you can retrieve p/q/r by calculating c1/c2/c3 - k % n
		"""

		v = int(input("Which one is your prime? Gimme your response: "))

		k1 = pow(v-x1, d, N)
		k2 = pow(v-x2, d, N)
		k3 = pow(v-x3, d, N)

		c1 = (k1+self.p) % N
		c2 = (k2+self.q) % N
		c3 = (k3+self.r) % N

		print("")
		print(f"c1 = {c1}")
		print(f"c2 = {c2}")
		print(f"c3 = {c3}")

class Story():

	def __init__(self):

		self.primeman = PrimeMan()
		self.pool = Pool()
		self.mercury = Mercury()

	def prologue(self):

		print("Yesterday, you received a ticket to the royal party from PrimeKing. You were afraid that someone would steal the ticket, so you encrpyted the ticket by unbreakable RSA!")
		self.ticket = random.randint(0, 1 << 1500)
		self.primeman.gen(512, self.ticket)
		self.primeman.throw_primes(self.pool)

	def menu(self):

		print("")
		print("[1] Look in your backpack")
		print("[2] Cry")
		print("[3] Jump into the pool")
		print("[4] Go to the party")
		print("[5] Exit")

		op = int(input(">>> "))
		return op

	def loop(self, n):

		for _ in range(n):

			op = self.menu()
			if op == 1:
				self.primeman.print_backpack()
			elif op == 2:
				if self.mercury:
					self.mercury.welcome_msg()
					self.mercury.find_primes(self.pool)
					self.mercury.oblivious()
					self.mercury = None
				else:
					print("")
					print("Mercury went back to the heaven ... ")
			elif op == 3:
				print("")
				print("Find nothing ...")
			elif op == 4:
				inp = int(input("Guard: Give me your ticket. "))

				if inp == self.ticket:
					with open("flag.txt", "r") as f:
						print("")
						print(f.read())
				else:
					print("")
					print("Go away!")
			elif op == 5:
				print("")
				print("Bye!")
				break

if __name__ == '__main__':

	signal.alarm(120)
	s = Story()
	s.prologue()
	s.loop(1337)
