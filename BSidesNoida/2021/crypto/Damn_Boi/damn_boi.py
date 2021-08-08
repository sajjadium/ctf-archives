#!/usr/bin/env python3
from Crypto.Util.number import *
from random import shuffle
from math import lcm, prod
from topsecrets import FLAG, FLAG_parts
from gmpy2 import next_prime

BITS = 512
FLAGINT = bytes_to_long(FLAG.encode())

assert FLAGINT == prod(FLAG_parts)


def pm(n):
    r = 1
    a = 2
    for i in range(n):
        r *= a
        a = next_prime(a)
    return r

def primegen(bits):
	e = 65537
	M = pm(40)

	while True:
		a = getPrime(128)
		b = getPrime(128)
		p = pow(e, a, M)
		q = pow(e, b, M)

		if isPrime(p) and isPrime(q):
			print(a,b)
			return int(p), int(q)

def keygen(bits, s):
    p,q = primegen(bits)
    n = p*q
    N = n**(s+1)
    print(f"{p=}")
    print(f"{q=}")
    d = lcm(p-1, q-1)
    x = getRandomRange(2, n-1)
    j = getRandomRange(2, n-1)
    while GCD(j, n) != 1:
        j = getRandomRange(2, n-1)
    g = pow(n+1, j, N)*x % N
    pub = (n,g,s)
    priv = (n,d)
    return pub, priv

def encrypt(m, pub):
    n, g, s = pub
    N = n**(s+1)
    r = getRandomRange(2, n-1)
    c = pow(g, m, N) * pow(r, n**s, N) % N
    return c

def encryptor(m, pub):
    n, g, s = pub
    N = n**(s+1)
    noise = [getRandomRange(2, N-1) for _ in range(len(FLAG_parts))]
    shuffle(FLAG_parts)
    enc = []
    for f, r in zip(FLAG_parts, noise):
        c = encrypt(f*r, pub)
        enc.append(c)
    shuffle(noise)
    return enc, noise

if __name__ == '__main__':
    pub, priv = keygen(BITS, 2)
    enc, noise = encryptor(FLAGINT, pub)

    with open('priv.txt', 'w') as out:
        out.write(f"{priv = }\n\n")

    with open('out.txt', 'w') as out:
        out.write(f"{pub = }\n\n")        
        out.write(f"{enc = }\n\n")
        out.write(f"{noise = }")

    