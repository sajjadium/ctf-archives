#!/usr/bin/env sage

from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import md5
from flag import flag

def gen_param(B):
	while True:
		a = randint(B >> 1, B)
		b = randint(B >> 2, B >> 1)
		p = 2**a * 3**b - 1
		if is_prime(p):
			return a, b

def gen_dmap(E):
	return E.isogeny(E.lift_x(ZZ(1)), codomain = E)

def gen_tpt(E, a, b):
	P, Q = [((p + 1) // 2**a) * _ for _ in E.gens()]
	R, S = [((p + 1) // 3**b) * _ for _ in E.gens()]
	return P, Q, R, S

def keygen(EC, b, P, Q, R, S):
	skey = randint(1, 3**b)
	T = R + skey * S
	phi = EC.isogeny(T, algorithm = "factored")
	_phi_dom, _phi_P, _phi_Q = phi.codomain(), phi(P), phi(Q)
	return skey, _phi_dom, _phi_P, _phi_Q

a, b = gen_param(190)
p = 2**a * 3**b - 1

F.<x> = GF(p^2, modulus = x**2 + 1)
EC = EllipticCurve(F, [0, 6, 0, 1, 0])
P, Q, R, S = gen_tpt(EC, a, b)

print(f'P = {P.xy()}')
print(f'Q = {Q.xy()}')
print(f'R = {R.xy()}')
print(f'S = {S.xy()}')

skey, _phi_dom, _phi_P, _phi_Q = keygen(EC, b, P, Q, R, S)

print(f'_phi_dom = {_phi_dom}')
print(f'_phi_P   = {_phi_P.xy()}')
print(f'_phi_Q   = {_phi_Q.xy()}')

key = md5(long_to_bytes(skey)).digest()
iv = md5(str(skey).encode()).digest()

cipher = AES.new(key, AES.MODE_CFB, iv=iv)
enc = cipher.encrypt(flag)

print(f'enc = {enc.hex()}')