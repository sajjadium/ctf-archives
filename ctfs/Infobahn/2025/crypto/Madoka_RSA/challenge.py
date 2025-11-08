from Crypto.Cipher import AES
from Crypto.Util.number import isPrime, getPrime
from Crypto.Util.Padding import pad
from hashlib import sha256
from os import getenv
from random import getrandbits
from sage.all import CRT, GF

class Madoka_RSA:
	@staticmethod
	def has_sqrt_2(p):
		return p % 8 == 1 or p % 8 == 7
	@staticmethod
	def sqrt_2(p):
		return int(GF(p)(2).sqrt())
	def __init__(self, nbit):
		while True:
			x = getrandbits(nbit)
			p = x**2 + x + 1
			q = 12 * x**2 + 12 * x + 7
			if isPrime(p) and self.has_sqrt_2(p) and isPrime(q) and self.has_sqrt_2(q):
				while True:
					r = getPrime(4 * nbit + 4)
					if self.has_sqrt_2(r):
						break
				break
		self.n = p * q * r
		self.e = 65537
		self.hint = CRT(
			[self.sqrt_2(p), self.sqrt_2(q), self.sqrt_2(r)],
			[p, q, r]
		)
	def encrypt(self, m):
		return pow(m, self.e, self.n)

if __name__ == "__main__":
	flag = getenv("FLAG", "infobahn{fake_flag}")

	nbit = 256
	MR = Madoka_RSA(nbit)
	secret = getrandbits(2000)

	print(MR.n)
	print(MR.e)
	print(MR.encrypt(secret))
	print(MR.hint)
	print(AES.new(sha256(hex(secret).encode()).digest()[:16], AES.MODE_ECB).encrypt(pad(flag.encode(), 16)).hex())
