from random import shuffle, randrange, randint
from os import urandom
from Crypto.Util.number import getPrime, getStrongPrime, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from private import flag
import sys

class RNG:
	def __init__(self, seed, a, b):
		self.state = seed
		self.a = a
		self.b = b
		print('a:', a)
		print('b:', b)

	def nextbits(self, bitlen):
		out = 0
		for _ in range(bitlen):
			out <<= 1
			self.state = self.a * self.state + b
			bit = int(sum(self.state[i] for i in range(7)))
			out += bit
		return out

def get_params(rng, bitlen):
	p = next_prime((1 << (bitlen - 1)) | rng.nextbits(bitlen))
	q = next_prime((1 << (bitlen - 1)) | rng.nextbits(bitlen))
	N = p * q
	return N, p, q

LIMIT = 26
P.<x> = PolynomialRing(GF(2))
F.<x> = P.quo(x^128 + x^7 + x^2 + x + 1)
key, a, b = [F.random_element() for _ in range(3)]
bytekey = long_to_bytes(int(''.join(list(map(str, key.list()))), 2))
iv = os.urandom(16)
cipher = AES.new(bytekey, AES.MODE_CBC, IV=iv)
rng = RNG(key, a, b)
N, p, q = get_params(rng, 512)
if randint(0, 1):
	p, q = q, p
e = 65537
d = inverse_mod(e, (p-1)*(q-1))
dp = d % (p-1)
r = getStrongPrime(1024)
g = randrange(2, r)
print('iv:', iv.hex())
print('N:', N)
print('e:', e)
print('g:', g)
print('r:', r)
print('encrypted flag:', cipher.encrypt(pad(flag, 16)).hex())
print()
print("now, let's cook some fried rice!")
for _ in range(LIMIT):
	sys.stdout.flush()
	m = int(input('add something in(in hex)> '), 16)
	dp ^^= m
	print('flip!', pow(g, dp, r))
print("it's done. enjoy your fried rice!")