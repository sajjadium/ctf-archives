from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
from os import getenv
from random import Random, getrandbits

class Sayaka_Stream:
	def __init__(self, seed):
		def make_generator(seed):
			rng = Random(seed)
			while True:
				x = rng.getrandbits(5)
				a, b, c, d, e = [x >> i & 1 for i in range(5)]
				yield int((a or not b or c == d or d != e) and (not a or b or c or d or not e))
		self.gen = make_generator(seed)
		self.generate_stream(10**5)
	def generate_stream(self, n):
		x = 0
		for i in range(n):
			x = x << 1 | next(self.gen)
		return x
	def generate_noise(self, seed, n):
		rng = Random(seed)
		noise = 0
		for dim_x, dim_y, dim_z in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
			plane = sum(1 << y * n**dim_y + z * n**dim_z for y in range(n) for z in range(n))
			for x in range(n):
				if rng.getrandbits(1):
					noise ^= plane << x * n**dim_x
		return noise
	def random_bits(self, n):
		noise_seed = self.generate_stream(1024)
		return self.generate_stream(n**3) ^ self.generate_noise(noise_seed, n)

if __name__ == "__main__":
	flag = getenv("FLAG", "infobahn{fake_flag}")
	assert flag.startswith("infobahn{") and flag.endswith("}")

	n = 42
	secret = getrandbits(19936)
	SS = Sayaka_Stream(secret)

	print(hex(SS.random_bits(n)))
	print(AES.new(sha256(hex(secret).encode()).digest()[:16], AES.MODE_ECB).encrypt(pad(flag.encode(), 16)).hex())
