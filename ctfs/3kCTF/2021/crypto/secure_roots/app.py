from Crypto.Util.number import getPrime, long_to_bytes
import hashlib, os, signal

def xgcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = xgcd(b % a, a)
		return (g, x - (b // a) * y, y)

def getprime():
	while True:
		p = getPrime(1024)
		if p % 4 == 3:
			return p
		

class Server():
	def __init__(self):
		self.private , self.public = self.gen()
		print("Prove your identity to get your message!\n")
		print("Public modulus : {}\n".format(self.public))
		
	def gen(self):
		p = getprime()
		q = getprime()
		return (p, q), p*q

	def decrypt(self, c):
		p, q = self.private
		mp = pow(c, (p+1)//4, p)
		mq = pow(c, (q+1)//4, q)
		_, yp, yq = xgcd(p, q)
		r = (yp * p * mq + yq * q * mp) % (self.public)
		return r

	def sign(self, m):
		U = os.urandom(20)
		c = int(hashlib.sha256(m + U).hexdigest(), 16)
		r = self.decrypt(c)
		return (r, int(U.hex(), 16))

	def verify(self, m, r, u):
		U = long_to_bytes(u)
		c = int(hashlib.sha256(m + U).hexdigest(), 16)
		return c == pow(r, 2, self.public)

	def get_flag(self):
		flag = int(open("flag.txt","rb").read().hex(), 16)
		return pow(flag, 0x10001, self.public)

	def login(self):
		m = input("Username : ").strip().encode()
		r = int(input("r : ").strip())
		u = int(input("u : ").strip())
		if self.verify(m, r, u):
			if m == b"Guest":
				print ("\nWelcome Guest!")
			elif m == b"3k-admin":
				print ("\nMessage : {}".format(self.get_flag()))
			else :
				print ("This user is not in our db yet.")
		else:
			print("\nERROR : Signature mismatch.")

if __name__ == '__main__':
	signal.alarm(10)
	S = Server()
	r, u = S.sign(b"Guest")
	print("Username : Guest\nr : {0}\nu : {1}\n".format(r , u))
	S.login()
