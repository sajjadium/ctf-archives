from math import gcd
from functools import reduce
from logger import Logger, noLog

class Montgomery:
	def __init__(self, modulus, log=noLog):
		self.n = modulus
		self.R = (1 << modulus.bit_length())# % modulus
		if gcd(self.n, self.R) != 1:
			raise Exception("[Err] Invalid modulus.")
		self.np = self.R - pow(self.n, -1, self.R)		#N': NN' = -1 mod R

		self.log=log

	def reduce(self, x):
		u = ((x % self.R) * self.np) % self.R
		t = (x + u * self.n) // self.R

		if t >= self.n:
			self.log.Verbose("[Montgomery] Extra reduction")
			return t - self.n
		else:
			return t

	def toMontgo(self, i):
		return (i * self.R) % self.n

	def redc(self, i):
		return self.reduce(i)

	def mul(self, x, y):
		return self.reduce(x*y)

def modExp(b, e, n, log=noLog):
	log.Info("[modExp] Normal -> Montgomery form...")
	m = Montgomery(n, log)
	r0 = m.toMontgo(1)
	r1 = m.toMontgo(b)

	l = e.bit_length()
	log.Info("[modExp] Repeated squaring")
	for i in range(l - 1, -1, -1):
		r0 = m.mul(r0, r0)
		if (e >> i) & 1 == 1:
			r0 = m.mul(r0, r1)

	log.Info("[modExp] Montgomery form -> Normal...")
	res = m.redc(r0)
	return res

def _modInv(a, b, log=noLog):
	if b == 1: return 1

	b0 = b
	x0, x1 = 0, 1

	while a > 1:
		q = a // b
		a, b = b, a % b
		x0, x1 = x1 - q * x0, x0

	if x1 < 0:
		x1 += b0

	return x1

def _crt(n, a, log=noLog):
	res = 0
	prod = reduce(lambda a, b: a* b, n)

	for ni, ai in zip(n, a):
		p = prod // ni

		log.Info("CRT: modular inverse")
		res += ai * _modInv(p, ni, log) * p

	return res % prod

def rsa_crt(c, d, p, q, log=noLog):
	log.Info("RSA CRT start.")
	log.Info("c1 = pow(c, d, p)")
	c1 = modExp(c % p, d % (p - 1), p, log)
	log.Info("c2 = pow(c, d, q)")
	c2 = modExp(c % q, d % (q - 1), q, log)

	log.Info("Applying CRT operation..")
	res = _crt([p, q], [c1, c2], log)

	return res
