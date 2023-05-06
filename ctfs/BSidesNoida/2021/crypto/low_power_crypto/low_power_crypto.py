from Crypto.Util.number import getRandomNBitInteger, isPrime


# extended gcd
def egcd(a, b):
	old_x, new_x = 1, 0
	old_y, new_y = 0, 1
	while a != 0:
		q, a, b = b // a, b % a, a
		new_x, old_x = old_x, new_x - q * old_x
		new_y, old_y = old_y, new_y - q * old_y
	return b, new_x, new_y


# multiplicative modular inverse
def modinv(a, m):
	g, x, _ = egcd(a % m, m)
	if g != 1:
		return None
	return x % m


# a class to represent a point on elliptic curve
class ec_point:
	def __init__(self, x, y, z=1):
		self.x = x
		self.y = y
		self.z = z

	def __repr__(self):
		if self.z == 0:
			return "<ORIGIN>"
		return f"<x={self.x}, y={self.y}>"


# a class to init an elliptic curve
class ec_curve:
	def __init__(self, p, r, a, b):
		self.p = p
		self.r = r
		self.a = a
		self.b = b
		assert isPrime(p) and isPrime(r)

	def __repr__(self):
		return f"elliptic curve y^2 = x^3 + {self.a}*x + {self.b} of order {self.r} over GF({self.p})"

	def is_origin(self, pt):
		return pt.z == 0

	# elliptic curve addition
	def add(self, pt1, pt2):
		if self.is_origin(pt1):
			return pt2
		if self.is_origin(pt2):
			return pt1
		if (pt1.y + pt2.y) % self.p == 0 and pt1.x == pt2.x:
			return self.origin()
		if pt1.x == pt2.x and pt1.y == pt2.y:
			temp = (((3 * pt1.x * pt1.x) + self.a) * modinv(2 * pt1.y, self.p)) % self.p
		else:
			temp = ((pt2.y - pt1.y) * modinv(pt2.x - pt1.x, self.p)) % self.p
		x = (temp * temp - pt1.x - pt2.x) % self.p
		y = (temp * (pt1.x - x) - pt1.y) % self.p
		return self(x, y)

	# multiplication using double and add
	def multiply(self, n, pt):
		if n == 0:
			return self.origin()
		curr_mult = pt
		res = self.origin()
		while n > 0:
			if n & 1:
				res = self.add(res, curr_mult)
			curr_mult = self.add(curr_mult, curr_mult)
			n = n >> 1
		return res

	# init a point on this curve
	# Usage:
	# curve = ec_curve(*params)
	# point = curve_name(x, y[, z])
	def __call__(self, x, y, z=1):
		res = ec_point(x % self.p, y % self.p, z)
		return res

	@staticmethod
	def origin():
		return ec_point(0, 1, 0)


if __name__ == "__main__":
	p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
	r = 115792089210356248762697446949407573529996955224135760342422259061068512044369
	a = 115792089210356248762697446949407573530086143415290314195533631308867097853948
	b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
	curve = ec_curve(p=p, r=r, a=a, b=b)
	print(curve)

	multiplier = getRandomNBitInteger(250)

	print("Because I am soo confident, I'll even let you make multiple public keys")
	print("Send points to multiply, or send <0,0> to move on:")

	try:

		for _ in range(10):

			x = int(input(">>> x coord => "))
			y = int(input(">>> y coord => "))

			if x == 0 and y == 0:
				break

			print(curve.multiply(multiplier, curve(x, y)))

		guess = int(input("multiplier => "))

		if guess == multiplier:
			print(open("flag.txt", "r").read())
		else:
			print("Never gonna give you up")

	except:
		print("Never gonna let you down")
