#!/usr/bin/env python3
import random
from decimal import Decimal,getcontext

class SeSeSe:
	def __init__(self, s, n, t):
		self.s = int.from_bytes(s.encode())
		self.l = len(s) 	
		self.n = n
		self.t = t
		self.a = self._a()

	def _a(self):
		c = [self.s]
		for i in range(self.t-1):
			a = Decimal(random.randint(self.s+1, self.s*2))
			c.append(a)
		return c

	def encode(self):
		s = []
		for j in range(self.n):
			x = j
			px = sum([self.a[i] * x**i for i in range(self.t)]) 
			s.append((x,px))
		return s

	def decode(self, shares):
		assert len(shares)==self.t
		secret = Decimal(0)
		for j in range(self.t):
			yj = Decimal(shares[j][1])
			r = Decimal(1)
			for m in range(self.t):
				if m == j:
					continue
				xm = Decimal(shares[m][0])
				xj = Decimal(shares[j][0])

				r *= Decimal(xm/Decimal(xm-xj))
			secret += Decimal(yj * r)
		return int(round(Decimal(secret),0)).to_bytes(self.l).decode()


if __name__ == "__main__":
	getcontext().prec = 256 # beat devision with precision :D 
	n = random.randint(50,150)
	t = random.randint(5,10)
	sss = SeSeSe(s=open("flag.txt",'r').read(), n=n, t=t)
	
	shares = sss.encode()

	print(f"Welcome to Sebastian's Secret Sharing!")
	print(f"I have split my secret into 1..N={sss.n} shares, and you need t={sss.t} shares to recover it.")
	print(f"However, I will only give you {sss.t-1} shares :P")
	for i in range(1,sss.t):
		try:
			sid = int(input(f"{i}.: Choose a share: "))
			if 1 <= sid <= sss.n:
				print(shares[sid % sss.n])
		except:
			pass
	print("Good luck!")