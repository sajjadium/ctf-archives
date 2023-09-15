from Crypto.Util.number import *
from Crypto.Cipher import AES
import random
import hashlib

def _hash(msg):
	return bytes_to_long(hashlib.sha1(msg).digest())

class LCG:
	def __init__(self, seed, q):
		self.q = q
		self.a = random.randint(2,self.q)
		self.b = random.randint(2,self.a)
		self.c = random.randint(2,self.b)
		self.d = random.randint(2,self.c)
		self.seed = seed

	def next(self):
		seed = (self.a*self.seed^3 + self.b*self.seed^2 + self.c*self.seed + self.d) % self.q
		self.seed = seed
		return seed

class ECDSA:
	def __init__(self, seed):
		self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
		self.E = EllipticCurve(GF(self.p), [0, 7])
		self.G = self.E.lift_x(55066263022277343669578718895168534326250603453777594175500187360389116729240)
		self.order = 115792089237316195423570985008687907852837564279074904382605163141518161494337

		self.priv_key = random.randint(2,self.order)
		self.pub_key = self.G*self.priv_key

		self.lcg = LCG(seed, self.order)

	def sign(self, msg):
		nonce = self.lcg.next()
		hashed = _hash(msg)

		r = int((self.G*nonce)[0]) % self.order
		assert r != 0
		s = (pow(nonce,-1,self.order)*(hashed + r*self.priv_key)) % self.order
		return (r,s)

	def verify(self, r, s, msg):
		assert r % self.order > 1
		assert s % self.order > 1

		hashed = _hash(msg)
		u1 = (hashed*pow(s,-1,self.order)) % self.order
		u2 = (r*pow(s,-1,self.order)) % self.order

		final_point = u1*self.G + u2*self.pub_key
		if int(final_point[0]) == r:
			return True
		else:
			return False
