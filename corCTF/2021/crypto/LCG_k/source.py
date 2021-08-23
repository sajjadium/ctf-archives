from Crypto.Util.number import bytes_to_long, inverse
from hashlib import sha256
from secrets import randbelow
from private import flag
from fastecdsa.curve import P256

G = P256.G
N = P256.q

class RNG:
	def __init__(self, seed, A, b, p):
		self.seed = seed
		self.A = A
		self.b = b
		self.p = p

	def gen(self):
		out = self.seed
		while True:
			out = (self.A*out + self.b) % self.p
			yield out

def H(m):
	h = sha256()
	h.update(m)
	return bytes_to_long(h.digest())

def sign(m):
	k = next(gen)
	r = int((k*G).x) % N
	s = ((H(m) + d*r)*inverse(k, N)) % N
	return r, s

def verify(r, s, m):
	v1 = H(m)*inverse(s, N) % N
	v2 = r*inverse(s, N) % N
	V = v1*G + v2*pub
	return int(V.x) % N == r

seed, A, b = randbelow(N), randbelow(N), randbelow(N)
lcg = RNG(seed, A, b, N)
gen = lcg.gen()
d = randbelow(N)
pub = d*G
mymsg = b'i wish to know the ways of the world'

print('public key:', pub)
signed_hashes = []

for _ in range(4):
	m = bytes.fromhex(input('give me something to sign, in hex>'))
	h = H(m)
	if m == mymsg or h in signed_hashes:
		print("i won't sign that.")
		exit()
	signed_hashes.append(h)
	r, s = sign(m)
	print('r:', str(r))
	print('s:', str(s))
print('now, i want you to sign my message.')
r = int(input('give me r>'))
s = int(input('give me s>'))
if verify(r, s, mymsg):
	print("nice. i'll give you the flag.")
	print(flag)
else:
	print("no, that's wrong.")