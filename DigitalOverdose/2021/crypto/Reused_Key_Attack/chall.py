import os
import hashlib
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random.random import getrandbits
from secret import flag

class LFSR:
	def __init__(self, key, taps):
		d = max(taps)
		assert len(key) == d, "Error: key of wrong size."
		self._s = key
		self._t = [d - t for t in taps]

	def _sum(self, L):
		s = 0
		for x in L:
			s ^= x
		return s

	def _clock(self):
		b = self._s[0]
		self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
		return b

	def bit(self):
		return self._clock()

class PRNG:
	def __init__(self, key, p, g):
		assert key.bit_length() <= 39
		key = [int(i) for i in list("{:039b}".format(key))]
		self.LFSR = [
			LFSR(key[:13], [13, 3, 1]),
			LFSR(key[13:26], [13, 9, 3]),
			LFSR(key[26:], [13, 9, 1]),
		]

		self.p = p
		self.g = g

	def coin(self):
		b = [lfsr.bit() for lfsr in self.LFSR]
		return b[1] if b[0] else b[2]

	def next(self):
		b = self.coin()
		k = random.randint(2, self.p)
		m = pow(33, 2 * k + b, self.p)
		x = random.randint(2, self.p)
		h = pow(self.g, x, self.p)
		y = random.randint(2, self.p)
		s = pow(h, y, self.p)
		c1 = pow(self.g, y, self.p)
		c2 = (s * m) % self.p
		return c2

def encrypt(key, flag):
	sha1 = hashlib.sha1()
	sha1.update(str(key).encode('ascii'))
	key = sha1.digest()[:16]
	iv = os.urandom(16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(pad(flag, 16))
	data = {
		"iv": iv.hex(),
		"enc": ciphertext.hex()
	}
	return data

key = getrandbits(39)
prng = PRNG(key, 8322374842981260438697208405030249462879, 3)
hint = [prng.next() for _ in range(133)]
print("hint = {}".format(hint))
print("enc = {}".format(encrypt(key, flag)))