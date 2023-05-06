from random import randrange
from Crypto.Util.number import getPrime, inverse, bytes_to_long, GCD

flag = b'dice{?????????????????????????}'
n = 5

def get_prime(n, b):
	p = getPrime(b)
	while GCD(p - 1, n) != 1:
		p = getPrime(b)
	return p

p = get_prime(n, 1024)
q = get_prime(n, 1024)
N = p*q
phi = (p - 1)*(q - 1)

e = 0xd4088c345ced64cbbf8444321ef2af8b
d = inverse(e, phi)

def sign(message):
	m = bytes_to_long(message)
	return pow(m, d, N)

def commit(s, key, n):
	return (s + key) % N, pow(key, n, N)

def reveal(c1, c2, key, n):
	assert pow(key, n, N) == c2
	return (c1 - key) % N

r = randrange(1, N)
s = sign(flag)
c1, c2 = commit(s, r, n)

print(f'N = {hex(N)}')
print(f'c1 = {hex(c1)}')
print(f'c2 = {hex(c2)}')