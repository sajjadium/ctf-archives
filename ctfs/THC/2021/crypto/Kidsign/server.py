from Crypto.Util.number import  inverse, isPrime
from random import SystemRandom
from hashlib import sha256
from flag import FLAG
import os

rand = SystemRandom()

class ElGamal:
	def __init__(self):
		self.q = 89666094075799358333912553751544914665545515386283824011992558231120286657213785559151513056027280869020616111209289142073255564770995469726364925295894316484503027288982119436576308594740674437582226015660087863550818792499346330713413631956572604302171842281106323020998625124370502577704273068156073608681
		assert(isPrime(self.q))
		self.p = 2*self.q + 1
		assert(isPrime(self.p))
		self.g = 2
		self.H = sha256
		self.x = rand.randint(1,self.p-2)
		self.y = pow(self.g,self.x,self.p)

	def sign(self,m):
		k = rand.randint(2,self.p-2)
		while GCD(k,self.p-1) != 1:
			k = rand.randint(2,self.p-2)
		r = pow(self.g,k,self.p)
		h = int(self.H(m).hexdigest(),16)
		s = ((h - self.x * r)* inverse(k,self.p-1)) % (self.p - 1)
		assert(s != 0)
		return (r,s)

	def verify(self,m,r,s):
		if r <= 0 or r >= (self.p):
			return False
		if s <= 0 or s >= (self.p-1):
			return False
		h = int(self.H(m).hexdigest(),16)
		return pow(self.g,h,self.p) == (pow(self.y,r,self.p) * pow(r,s,self.p)) % self.p



if __name__ == '__main__':
	S = ElGamal()

	print("Here are your parameters:\n - generator g: {:d}\n - prime p: {:d}\n - public key y: {:d}\n".format(S.g, S.p, S.y))
	
	message = os.urandom(16)

	print("If you can sign this message : {:s}, I'll reward you with a flag!".format(message.hex()))

	r = int(input("r: "))
	s = int(input("s: "))
	if S.verify(message,r,s):
		print(FLAG)
	else:
		print("Nope.")
