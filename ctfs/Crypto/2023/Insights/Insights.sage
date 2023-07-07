#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def getRandomNBits(n):
	nb = '1' + ''.join([str(randint(0, 1)) for _ in range(n - 1)])
	return nb

def getLeader(L, n):
	nb = L + getRandomNBits(n)
	return int(nb, 2)

def genPrime(L, nbit):
	l = len(L)
	assert nbit >= l
	while True:
		p = getLeader(L, nbit - l)
		if is_prime(p):
			return p

def genKey(L, nbit):
	p, q = [genPrime(L, nbit) for _ in '__']
	n = p * q
	d = next_prime(pow(n, 0.2919))
	phi = (p - 1) * (q - 1)
	e = inverse(d, phi)
	pubkey, privkey = (n, e), (p, q)
	return pubkey, privkey

def encrypt(msg, pubkey):
	n, e = pubkey
	m = bytes_to_long(msg)
	c = pow(m, e, n)
	return c

nbit = 1024
L = bin(bytes_to_long(b'Practical'))[2:]
pubkey, privkey = genKey(L, nbit)
p, q = privkey
c = encrypt(flag, pubkey)

print('Information:')
print('-' * 85)
print(f'n = {p * q}')
print(f'e = {pubkey[1]}')
print(f'c = {c}')
print(f'p = {bin(p)[2:len(L)]}...[REDACTED]')
print(f'q = {bin(q)[2:len(L)]}...[REDACTED]')
print('-' * 85)
