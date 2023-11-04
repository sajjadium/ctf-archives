#!/usr/bin/env -S python3 -u
import os
from Crypto.Util.number import isPrime, bytes_to_long
from Crypto.Random.random import randrange
class Point:
	def __init__(self,x,y,curve, isInfinity = False):
		self.x = x % curve.p
		self.y = y % curve.p
		self.curve = curve
		self.isInfinity = isInfinity
	def __add__(self,other):
		return self.curve.add(self,other)
	def __mul__(self,other):
		return self.curve.multiply(self,other)
	def __rmul__(self,other):
		return self.curve.multiply(self,other)
	def __str__(self):
		return f"({self.x},{self.y})"
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.curve == other.curve
class Curve:
	def __init__(self,a,b,p):
		if (4*pow(a,3,p)+27*pow(b,2,p)) %p == 0:
			print("Error : 4a^3+27b^2 = 0")
			quit()
		if p < 1 or not isPrime(p):
			print("p needs to be prime ")
			quit()

		self.a = a%p
		self.b = b%p
		self.p = p
	def multiply(self, P:Point, k:int) -> Point:
		Q = P
		R = Point(0,0,self,isInfinity=True)
		while k > 0 :
			if (k & 1) == 1:
				R = self.add(R,Q)
			Q = self.add(Q,Q)
			k >>= 1
		return R
	def find_y(self,x):
		# p is 3 mod 4 in NIST-192-P so easy to find y
		x = x % self.p
		y_squared = (pow(x, 3, self.p) + self.a * x + self.b) % self.p
		assert pow(y_squared, (self.p - 1) // 2, self.p) == 1, "The x coordinate is not on the curve"
		y = pow(y_squared, (self.p + 1) // 4, self.p)
		assert pow(y,2,self.p) == (pow(x, 3, self.p) + self.a * x + self.b) % self.p
		return y

	def add(self,P: Point, Q : Point) -> Point:
		if P.isInfinity:
			return Q
		elif Q.isInfinity:
			return P
		elif P.x == Q.x and P.y == (-Q.y) % self.p:
			return Point(0,0,self,isInfinity=True)
		if P.x == Q.x and P.y == Q.y:
			param = ((3*pow(P.x,2,self.p)+self.a) * pow(2*P.y,-1,self.p))
		else:
			param = ((Q.y - P.y) * pow(Q.x-P.x,-1,self.p))
		Sx =  (pow(param,2,self.p)-P.x-Q.x)%self.p
		Sy = (param * ((P.x-Sx)%self.p) - P.y) % self.p
		return Point(Sx,Sy,self)


p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
curve = Curve(a,b,p)
flag = os.getenv("flag","EPFL{fake_flag}")
flag = bytes_to_long(flag.encode())
G = Point(flag,curve.find_y(flag),curve)
PK = randrange(1,p)
pub = PK * G
print(f"""Welcome to KeySharer™ using that good old NIST 192-P
=============================================
Alice wants to share her public key with you so that you both can have multiple shared secret keys !
Alice's public key is {pub}
Now send over yours !
""")
for i in range(4):
	your_pub_key_x = int(input(f"Gimme your pub key's x : \n"))
	your_pub_key_y = int(input(f"Gimme your pub key's y : \n"))
	your_pub_key = Point(your_pub_key_x,your_pub_key_y,curve)
	shared_key = your_pub_key * PK
	print(f"The shared key is\n {shared_key}")
