#!/usr/local/bin/python
from Crypto.Util.number import getPrime, inverse, bytes_to_long
from random import randrange

with open("flag.txt", "rb") as f:
	flag = f.read().strip()

def gen_keypair():
	p, q = getPrime(512), getPrime(512)
	n = (p**2) * q
	while True:
		g = randrange(2, n)
		if pow(g, p-1, p**2) != 1:
			break
	h = pow(g, n, n)
	return (n, g, h), (g, p, q)

def encrypt(pubkey, m):
	n, g, h = pubkey
	r = randrange(1, n)
	c = pow(g, m, n) * pow(h, r, n) % n
	return c

def decrypt(privkey, c):
	g, p, q = privkey
	a = (pow(c, p-1, p**2) - 1) // p
	b = (pow(g, p-1, p**2) - 1) // p
	m = a * inverse(b, p) % p
	return m

def oracle(privkey, c):
	m = decrypt(privkey, c)
	return m % 2

pub, priv = gen_keypair()
n, g, h = pub
print(f"Public Key:\n{n = }\n{g = }\n{h = }")
print(f"Encrypted Flag: {encrypt(pub, bytes_to_long(flag))}")
while True:
	inp = int(input("Enter ciphertext> "))
	print(f"Oracle result: {oracle(priv, inp)}")