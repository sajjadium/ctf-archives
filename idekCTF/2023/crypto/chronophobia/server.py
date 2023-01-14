#!/usr/bin/env python3

from Crypto.Util.number import *
import random
import signal

class PoW():

	def __init__(self, kbits, L):

		self.kbits = kbits
		self.L = L

		self.banner()
		self.gen()
		self.loop(1337)

	def banner(self):

		print("===================================")
		print("=== Welcome to idek PoW Service ===")
		print("===================================")
		print("")

	def menu(self):

		print("")
		print("[1] Broken Oracle")
		print("[2] Verify")
		print("[3] Exit")
		
		op = int(input(">>> "))
		return op

	def loop(self, n):

		for _ in range(n):

			op = self.menu()
			if op == 1:
				self.broken_oracle()			
			elif op == 2:
				self.verify()
			elif op == 3:
				print("Bye!")
				break

	def gen(self):

		self.p = getPrime(self.kbits)
		self.q = getPrime(self.kbits)
		
		self.n = self.p * self.q
		self.phi = (self.p - 1) * (self.q - 1)

		t = random.randint(0, self.n-1)
		print(f"Here is your random token: {t}")
		print(f"The public modulus is: {self.n}")

		self.d = random.randint(128, 256)
		print(f"Do 2^{self.d} times exponentiation to get the valid ticket t^(2^(2^{self.d})) % n!")

		self.r = pow(2, 1 << self.d, self.phi)
		self.ans = pow(t, self.r, self.n)

		return

	def broken_oracle(self):

		u = int(input("Tell me the token. "))
		ans = pow(u, self.r, self.n)
		inp = int(input("What is your calculation? "))
		if ans == inp:
			print("Your are correct!")
		else:
			print(f"Nope, the ans is {str(ans)[:self.L]}... ({len(str(ans)[self.L:])} remain digits)")

		return

	def verify(self):

		inp = int(input(f"Give me the ticket. "))		
       
		if inp == self.ans:
			print("Good :>")
			with open("flag.txt", "rb") as f:
				print(f.read())
		else:
			print("Nope :<")

if __name__ == '__main__':

	signal.alarm(120)
	service = PoW(512, 200)
    
