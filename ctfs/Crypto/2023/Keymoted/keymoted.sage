#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def gen_koymoted(nbit):
	p = getPrime(nbit)
	a, b = [randint(1, p - 1) for _ in '__']
	Ep = EllipticCurve(GF(p), [a, b])
	tp = p + 1 - Ep.order()
	_s = p ^^ ((2 ** (nbit - 1)) + 2 ** (nbit // 2))
	q = next_prime(2 * _s + 1)
	Eq = EllipticCurve(GF(q), [a, b])
	n = p * q
	tq = q + 1 - Eq.order()
	e = 65537
	while True:
		if gcd(e, (p**2 - tp**2) * (q**2 - tq**2)) == 1:
			break
		else:
			e = next_prime(e)
	pkey, skey = (n, e, a, b), (p, q)
	return pkey, skey

def encrypt(msg, pkey, skey):
	n, e, a, b = pkey
	p, q = skey
	m = bytes_to_long(msg)
	assert m < n
	while True:
		xp = (m**3 + a*m + b) % p
		xq = (m**3 + a*m + b) % q
		if pow(xp, (p-1)//2, p) == pow(xq, (q-1)//2, q) == 1:
			break
		else:
			m += 1
	eq1, eq2 = Mod(xp, p), Mod(xq, q)
	rp, rq = sqrt(eq1), sqrt(eq2)
	_, x, y = xgcd(p, q)
	Z = Zmod(n)
	x = (Z(rp) * Z(q) * Z(y) + Z(rq) * Z(p) * Z(x)) % n
	E = EllipticCurve(Z, [a, b])
	P = E(m, x)
	enc = e * P
	return enc

nbit = 256
pkey, skey = gen_koymoted(nbit)
enc = encrypt(flag, pkey, skey)

print(f'pkey = {pkey}')
print(f'enc = {enc}')