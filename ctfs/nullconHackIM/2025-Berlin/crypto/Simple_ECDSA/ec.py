#!/usr/bin/env python3
def inverse(a,n):
	return pow(a,-1,n)

class EllipticCurve(object):
	def __init__(self, p, a, b, order = None):
		self.p = p
		self.a = a
		self.b = b
		self.n = order

	def __str__(self):
		return 'y^2 = x^3 + %dx + %d modulo %d' % (self.a, self.b, self.p)

	def __eq__(self, other):
		return (self.a, self.b, self.p) == (other.a, other.b, other.p)

class ECPoint(object):
	def __init__(self, curve, x, y, inf = False):
		self.x = x % curve.p
		self.y = y % curve.p
		self.curve = curve
		if inf or not self.is_on_curve():
			self.inf = True
			self.x = 0
			self.y = 0
		else:
			self.inf = False

	def is_on_curve(self):
		return self.y**2 % self.curve.p == (self.x**3 + self.curve.a*self.x + self.curve.b) % self.curve.p

	def copy(self):
		return ECPoint(self.curve, self.x, self.y)
	
	def __neg__(self):
		return ECPoint(self.curve, self.x, -self.y, self.inf)

	def __add__(self, point):
		p = self.curve.p
		if self.inf:
			return point.copy()
		if point.inf:
			return self.copy()
		if self.x == point.x and (self.y + point.y) % p == 0:
			return ECPoint(self.curve, 0, 0, True)
		if self.x == point.x:
			lamb = (3*self.x**2 + self.curve.a) * inverse(2 * self.y, p) % p
		else:
			lamb = (point.y - self.y) * inverse(point.x - self.x, p) % p
		x = (lamb**2 - self.x - point.x) % p
		y = (lamb * (self.x - x) - self.y) % p
		return ECPoint(self.curve,x,y)

	def __sub__(self, point):
		return self + (-point)

	def __str__(self):
		if self.inf: return 'Point(inf)'
		return 'Point(%d, %d)' % (self.x, self.y)

	def __mul__(self, k):
		k = int(k)
		base = self.copy()
		res = ECPoint(self.curve, 0,0,True)
		while k > 0:
			if k & 1:
				res = res + base
			base = base + base
			k >>= 1
		return res

	def __eq__(self, point):
		return (self.inf and point.inf) or (self.x == point.x and self.y == point.y)

if __name__ == '__main__':
	p = 17
	a = -1
	b = 1
	curve = EllipticCurve(p,a,b)
	P = ECPoint(curve, 1, 1)
	print(P+P)
