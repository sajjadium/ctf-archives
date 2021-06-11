from Crypto.Util.number import *
from gmpy2 import legendre

def generate():
	p = getStrongPrime(1024)
	q = getStrongPrime(1024)
	n = p*q
	x = getRandomRange(0, n)
	while legendre(x, p) != -1 or legendre(x, q) != -1:
		x = getRandomRange(0, n)
	return (n, x), (p, q)

def encrypt(m, pk):
	n, x = pk
	for b in format(int(m.encode('hex'), 16), 'b').zfill(len(m) * 8):
		y = getRandomRange(0, n)
		yield pow(y, 2) * pow(x, int(b)) % n

def decrypt(c, sk):
	p, q = sk
	m = 0
	for z in c:
		m <<= 1
		if legendre(z % p, p) != 1 or legendre(z % q, q) != 1:
			m += 1
	h = '%x' % m
	l = len(h)
	return h.zfill(l + l % 2).decode('hex')