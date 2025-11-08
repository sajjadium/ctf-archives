from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad
from copy import deepcopy
from hashlib import sha256
from itertools import product
from os import getenv
from random import getrandbits, randrange

class Kyoko_Ring:
	def __init__(self, p, q, data):
		for i, j in product(range(3), repeat = 2):
			assert 0 <= data[i][j] < p**(i + 1) * q**(j + 1)
			assert data[i][j] % (p**max(0, i - j) * q**max(0, j - i)) == 0
		self.p = p
		self.q = q
		self.data = deepcopy(data)
	@staticmethod
	def random_element(p, q):
		data = [
			[       randrange(p * q), q * randrange(p    * q   ), q**2 * randrange(p    * q   )],
			[p    * randrange(p * q),     randrange(p**2 * q**2), q    * randrange(p**2 * q**2)],
			[p**2 * randrange(p * q), p * randrange(p**2 * q**2),        randrange(p**3 * q**3)],
		]
		return Kyoko_Ring(p, q, data)
	@staticmethod
	def multiplicative_identity(p, q):
		data = [
			[1, 0, 0],
			[0, 1, 0],
			[0, 0, 1],
		]
		return Kyoko_Ring(p, q, data)
	def __mul__(self, other):
		data = [[0] * 3 for _ in range(3)]
		for i, j, k in product(range(3), repeat = 3):
			data[i][k] += self.data[i][j] * other.data[j][k]
		for i, j in product(range(3), repeat = 2):
			data[i][j] %= self.p**(i + 1) * self.q**(j + 1)
		return Kyoko_Ring(self.p, self.q, data)
	def __pow__(self, expo):
		assert 0 <= expo
		res = Kyoko_Ring.multiplicative_identity(self.p, self.q)
		base = Kyoko_Ring(self.p, self.q, self.data)
		while expo:
			if expo & 1:
				res *= base
			base *= base
			expo >>= 1
		return res
	def __repr__(self):
		return str(self.data)

if __name__ == "__main__":
	flag = getenv("FLAG", "infobahn{fake_flag}")

	p, q = getPrime(100), getPrime(100)
	g = Kyoko_Ring.random_element(p, q)
	secret = getrandbits(580)

	print(g)
	print(g**secret)
	print(AES.new(sha256(hex(secret).encode()).digest()[:16], AES.MODE_ECB).encrypt(pad(flag.encode(), 16)).hex())
