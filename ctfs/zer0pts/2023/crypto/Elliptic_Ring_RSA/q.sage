import string
import random

flag = os.environb.get(b"FLAG", b"dummmmy{test_test_test}")

class EllipticRingElement:
	point = None
	def __init__(self, point):
		self.point = point
	
	def __add__(self, other):
		if self.point == dict():
			return other
		if other.point == dict():
			return self
		res = self.point.copy()
		for k in other.point.keys():
			if k in res:
				res[k] += other.point[k]
				if res[k] == 0:
					res.pop(k)
			else:
				res[k] = other.point[k]
				if res[k] == 0:
					res.pop(k)
		return EllipticRingElement(res)
	
	def __mul__(self, other):
		if self.point == dict() or other.point == dict():
			return self.point()
		res = dict()
		for k1 in other.point.keys():
			for k2 in self.point.keys():
				E = k1 + k2
				k = other.point[k1] * self.point[k2]
				if E in res:
					res[E] += k
					if res[E] == 0:
						res.pop(E)
				else:
					res[E] = k
					if res[E] == 0:
						res.pop(E)
		return EllipticRingElement(res)
	
	def __repr__(self):
		st = ""
		for k in self.point.keys():
			st += f"{self.point[k]}*({k[0]}, {k[1]}) + "
		return st[:-3]
	
class EllipticRing:
	E = None
	Base = None
	def __init__(self, E):
		self.E = E
		self.Base = E.base()

	def __call__(self, pt):
		for P in pt:
			pt[P] = self.Base(pt[P])
		return EllipticRingElement(pt)
	
	def zero(self):
		return EllipticRingElement(dict())
	
	def one(self):
		return EllipticRingElement({E(0): self.Base(1)})
	
	def pow(self, x, n):
		res = self.one()
		while n:
			if (n & 1):
				res = res * x
			x = x * x
			n >>= 1
		return res
	
	def encode(self, m, length):
		left = random.randint(0, length - len(m))
		pad1 = "".join(random.choices(string.ascii_letters, k=left)).encode("utf-8")
		pad2 = "".join(random.choices(string.ascii_letters, k=length-len(m)-left)).encode("utf-8")
		m = pad1 + m + pad2

		Ps = []
		while len(Ps) < length:
			PP = self.E.random_element()
			if PP not in Ps:
				Ps.append(PP)
		Ps = sorted(Ps)

		M = dict()
		for coef, pt in zip(m, Ps):
			M[pt] = self.Base(coef)
		return EllipticRingElement(M)
	
def random_prime_bits(nbits):
	return random_prime(2^nbits-1, false, 2^(nbits-1))

nbits = 8
p = random_prime_bits(nbits)
Fp = GF(p)

a = Fp.random_element()
b = Fp.random_element()
E = EllipticCurve(Fp, [a, b])

ER = EllipticRing(E)

P = ER.encode(flag, 30)

e = 13
C = ER.pow(P, e)

print(f"p: {p}")
print(f"C: {C}")
print(f"a: {a}")
print(f"b: {b}")
print(f"e: {e}")
