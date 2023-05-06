from gmpy2 import div, gcd, invert, powmod

from Crypto.Util.number import getPrime, getRandomRange

def unpack(fn):
	with open(fn, 'r') as f:
		return tuple([int(x) for x in f.readlines()])

def pack(fn, k):
	with open(fn, 'w') as f:
		f.write('\n'.join([str(x) for x in k]))

def generate():
	r = 257
	while True:
		p = getPrime(1024)
		if (p-1) % r == 0 and gcd(r, div(p-1, r)) == 1:
			break
	while True:
		q = getPrime(1024)
		if gcd(r, q-1) == 1:
			break
	n = p*q
	phi = (p-1)*(q-1)
	while True:
		y = getRandomRange(0, n)
		x = powmod(y, phi*invert(r, n) % n, n)
		if x != 1:
			break
	return (n, y), (n, phi, x)

def encrypt(m, pk):
	r = 257
	n, y = pk
	u = getRandomRange(0, n)
	return powmod(y, m, n)*powmod(u, r, n) % n

def decrypt(c, sk):
	r = 257
	n, phi, x = sk
	a = powmod(c, phi*invert(r, n) % n, n)
	for i in range(256):
		if powmod(x, i, n) == a:
			return i
	return 0