from Crypto.Random.random import randrange
from Crypto.Util.number import getPrime, GCD

r = 17

def keygen():
	while True:
		p = getPrime(1024)
		a, b = divmod(p-1, r)
		if b == 0 and GCD(r, a) == 1:
			break
	while True:
		q = getPrime(1024)
		if GCD(r, q-1) == 1:
			break
	n = p*q
	phi = (p-1)*(q-1)//r
	y = 1
	while True:
		y = randrange(n)
		x = pow(y, phi, n)
		if x != 1:
			break
	log = {pow(x, i, n): i for i in range(r)}
	return (n, y), (n, phi, log)

def encrypt(data, pk):
	n, y = pk
	u = randrange(n)
	a = randrange(n)
	c = randrange(n)
	for m in data.hex():
		yield pow(y, int(m, 16), n) * pow(u, r, n) % n
		u = (a*u + c) % n

def decrypt(data, sk):
	n, phi, log = sk
	return bytes.fromhex(''.join(f'{log[pow(z, phi, n)]:x}' for z in data))

if __name__ == '__main__':
	from local import flag
	pk, sk = keygen()
	print(pk)
	for z in encrypt(flag, pk):
		print(z)
