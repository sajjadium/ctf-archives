from Crypto.Util.number import getPrime, long_to_bytes
from pwn import *
import random, binascii

flag = open('flag.txt').read()

def v(p, k):
	ans = 0
	while k % p == 0:
		k /= p
		ans += 1
	return ans

p, q, r = getPrime(2048), getPrime(2048), getPrime(2048)
print(p, q, r)
n = pow(p, q) * r

a1 = random.randint(0, n)
a2 = n - a1
assert a1 % p != 0 and a2 % p != 0

t = pow(a1, n) + pow(a2, n)
print(binascii.hexlify(xor(flag, long_to_bytes(v(p, t)))))



