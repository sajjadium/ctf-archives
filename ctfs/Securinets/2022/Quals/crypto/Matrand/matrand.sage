from Crypto.Util.number import bytes_to_long, getStrongPrime
from Crypto.Util.Padding import pad
import random

FLAG = b"Securinets{REDACTED}"
FLAG = FLAG.lstrip(b"Securinets{").rstrip(b"}")
assert len(FLAG)*8 < 2^392

class Random():
	def __init__(self, p, taps):
		self.p = p
		self.taps = taps
		self.seed_x = [random.randrange(1, self.p-1) for _ in range(3)]

	def reseed(self, x):
		self.seed_x = self.seed_x[1:] + [x]

	def next(self):
		x = (self.taps[0]*self.seed_x[0] + self.taps[1]*self.seed_x[1] + self.taps[2]*self.seed_x[2]) % p
		self.reseed(x)
		return x

p = 0xfa667a4f92149261c2d9a7d1e43d5a83a4342d880b6ddfbe40072d3f439eb917a2815564090fef8087fbdfeb51e9977603ad91a3317ec3754554f8da472747c5
taps = [random.randrange(1, p-1) for _ in range(3)]
R = Random(p, taps)

w = []
msgs = [pad(FLAG, 64), os.urandom(64)]
for msg in msgs:
	v = vector(GF(p), [bytes_to_long(msg[i:i+16]) for i in range(0, len(msg), 16)])
	while True:
		M = Matrix(GF(p), [[R.next() for i in range(4)] for j in range(4)])
		if M.det() == 0:
			break
	w.append(list(M*v))

print(f"{msgs[1].hex()}")
print(f"taps = {taps}")
print(f"w = {w}")