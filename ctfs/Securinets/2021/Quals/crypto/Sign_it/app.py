from Crypto.Util.number import inverse
from Crypto.Random import random
from fastecdsa.curve import Curve
from fastecdsa.point import Point
import hashlib
import signal

class Server():
	def __init__(self, curve, G):
		self.G = G
		self.order = curve.q
		self.d = random.randrange(1 , self.order - 1)
		self.P = (self.d * self.G)

	def sign(self, msg):
		z = int( hashlib.sha256(msg.encode()).hexdigest(), 16)
		k = random.randrange(1, self.order - 1)
		r = (k * self.G).x % self.order
		s = (inverse(k, self.order) * (z + r * self.d)) % self.order
		return (r, s)

	def verify(self, msg, sig):
		r, s = sig
		s %= self.order
		r %= self.order
		if s == 0 or r == 0:
			return False
		z = int( hashlib.sha256(msg.encode()).hexdigest(), 16)
		s_inv = inverse(s, self.order)
		u1 = (z * s_inv) % self.order
		u2 = (r * s_inv) % self.order
		W = u1 * self.G + u2 * self.P
		return W.x == r

signal.alarm(360)
# S256 curve params
p = 0x402969301d0ec23afaf7b6e98c8a6aebb286a58f525ec43b46752bfc466bc435
gx = 0x3aedc2917bdb427d67322a1daf1073df709a1e63ece00b01530511dcb1bae0d4
gy = 0x21cabf9609173616f5f50cb83e6a5673e4ea0facdc00d23572e5269632594f1d
a = 0x2ad2f52f18597706566e62f304ae1fa48e4062ee8b7d5627d6f41ed24dd68b97
b = 0x2c173bd8b2197e923097541427dda65c1c41ed5652cba93c86a7d0658070c707
q = 0x402969301d0ec23afaf7b6e98c8a6aeb2f4b05d0bbb538c027395fa703234883
S256 = Curve("S256", p, a, b, q, gx, gy)

PROOF = "Give me flag."
print("Welcome to the ECDSA testing of our probably secure S256 Curve. First choose your own generator then try to sign this message '{}' to prove us wrong.\n".format(PROOF))

print("Choose your point (x y) : ")

try:
	x = int(input("x : "))
	y = int(input("y : "))
	G = Point(x, y, curve=S256)
	S = Server(S256, G)

	sample = "No flags for you."
	print("Here's a sample signature: msg = '{}' , signature = {}".format(sample, S.sign(sample)))

	while True:
		msg = input("Message : ").strip()
		r = int(input("r : "))
		s = int(input("s : "))
		if S.verify(msg, (r, s)):
			print("Valid signature.")
			if msg == PROOF:
				from secret import flag
				print("Here you go : {}".format(flag))
				exit()
		else:
			print("Invalid signature.")

except Exception as e:
	print(e)
	exit()