#!/usr/local/bin/python

import secrets
import sys
from hashlib import scrypt, shake_256
from sibc.sidh import SIDH, default_parameters

sidh = SIDH(**default_parameters)
xor = lambda x, y: bytes(map(int.__xor__, x, y))
H = lambda x: shake_256(x).digest(16)
G = lambda x: shake_256(x).digest((3**sidh.strategy.three).bit_length() // 8)

def is_equal(x, y):
	# let's simulate a timing attack!
	c = secrets.randbelow(64)
	equal = True
	for a, b in zip(x, y):
		c += 1
		if a != b:
			equal = False
			break
	print(f'took {c} units of time')
	return equal

class KEM:
	def __init__(self, pk, sk=None):
		self.pk = pk
		self.sk = sk

	@classmethod
	def generate(cls):
		sk, pk = sidh.keygen_a()
		sk += secrets.token_bytes(16)
		return cls(pk, sk)

	def _encrypt(self, m, r):
		c0 = sidh.public_key_b(r)
		j = sidh.dh_b(r, self.pk)
		h = H(j)
		c1 = xor(h, m)
		return c0, c1

	def _decrypt(self, c0, c1):
		j = sidh.dh_a(self.sk[:-16], c0)
		h = H(j)
		m = xor(h, c1)
		return m

	def encapsulate(self):
		m = secrets.token_bytes(16)
		r = G(m + self.pk)
		c0, c1 = self._encrypt(m, r)
		ct = c0 + c1
		ss = H(m + ct)
		return ct, ss

	def decapsulate(self, ct):
		if self.sk is None:
			raise ValueError('no private key')

		if len(ct) != 6*sidh.p_bytes + 16:
			raise ValueError('malformed ciphertext')

		m = self._decrypt(ct[:-16], ct[-16:])
		r = G(m + self.pk)
		c0 = sidh.public_key_b(r)
		if is_equal(c0, ct[:-16]):
			ss = H(m + ct)
		else:
			ss = H(self.sk[-16:] + ct)
		return ss

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'init':
		kem = KEM.generate()
		with open('pk.bin', 'wb') as f:
			f.write(kem.pk)
		with open('sk.bin', 'wb') as f:
			f.write(kem.sk)
		with open('flag.txt', 'rb') as f:
			flag = f.read().strip()
		with open('flag.enc', 'wb') as f:
			key = scrypt(kem.sk[:-16], salt=b'defund', n=1048576, r=8, p=1, maxmem=1073744896, dklen=len(flag))
			f.write(xor(key, flag))
		exit()

	with open('pk.bin', 'rb') as f:
		pk = f.read()
	with open('sk.bin', 'rb') as f:
		sk = f.read()
	kem = KEM(pk, sk=sk)
	ct = bytes.fromhex(input('ct (hex): '))
	print('decapsulating...')
	ss = kem.decapsulate(ct)
	print(f'ss (hex): {ss.hex()}')
