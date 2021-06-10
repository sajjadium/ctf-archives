import numpy as np
from random import SystemRandom
from shake import ShakeRandom
from Crypto.Hash import SHAKE128

system = SystemRandom()

n = 640
q = 1 << 16
sigma = 2.8
bound = 6000

def pack(*values):
	data = bytes()
	for x in values:
		data += x.tobytes()
	return data

def unpack(data, width=1):
	for i in range(0, len(data), n*width*2):
		yield np.ndarray((n, width), dtype=np.uint16, buffer=data, offset=i)

def uniform(random=system, width=1):
	sample = lambda *_: random.randrange(q)
	return np.fromfunction(np.vectorize(sample), (n, width)).astype(np.uint16)

def gauss(random=system, width=1):
	sample = lambda *_: round(random.gauss(0, sigma)) % q
	return np.fromfunction(np.vectorize(sample), (n, width)).astype(np.uint16)

def short(x):
	return np.linalg.norm(np.minimum(x, -x)) < bound

class Key:
	def __init__(self, a, b, s=None):
		self.a = a
		self.b = b
		self.s = s

	@classmethod
	def generate(cls):
		a = uniform(width=n)
		s = gauss(width=n)
		b = a @ s + gauss(width=n)
		return cls(a, b, s)

	@classmethod
	def deserialize(cls, data):
		return cls(*unpack(data, width=n))

	def serialize(self, private=False):
		if private:
			return pack(self.a, self.b, self.s)
		else:
			return pack(self.a, self.b)

	def sign(self, message):
		s = gauss()
		b = self.a @ s + gauss()
		c = gauss(random=ShakeRandom(pack(self.a, self.b, b) + message))
		r = s - self.s @ c
		return pack(b, r)

	def verify(self, message, signature):
		b, r = unpack(signature)
		assert short(r)
		c = gauss(random=ShakeRandom(pack(self.a, self.b, b) + message))
		assert short(self.a @ r + self.b @ c - b)

if __name__ == '__main__':
	message = b'silly sheep'
	key = Key.generate()

	with open('public.key', 'wb') as f:
		f.write(key.serialize())

	with open('private.key', 'wb') as f:
		f.write(key.serialize(private=True))

	with open('signatures.bin', 'wb') as f:
		for _ in range(1337):
			signature = key.sign(message)
			key.verify(message, signature)
			f.write(signature)
