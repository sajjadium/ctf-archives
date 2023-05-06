#!/usr/local/bin/python -u

from Crypto.Util.number import *

N = 1024
p = getPrime(N)
q = getPrime(N)
assert GCD(p * q, (p - 1) * (q - 1)) == 1

n = p * q
s = n ** 2
λ = (p - 1) * (q - 1) // GCD(p - 1, q - 1)
g = getRandomRange(1, s)
L = lambda x : (x - 1) // n
μ = pow(L(pow(g, λ, s)), -1, n)

def encrypt(m):
    r = getRandomRange(1, n)
    c = (pow(g, m, s) * pow(r, n, s)) % (s)
    return c

def decrypt(c):
    m = (L(pow(c, λ, s)) * μ) % n
    return m

print(f"public key (n, g) = ({n}, ?)")
print(f"E(4) = {encrypt(4)}")
print()
print("Encrypt 'Please give me the flag' for your flag:")
c = int(input())
m = decrypt(c)

if long_to_bytes(m) == b"Please give me the flag":
    print("Okay!")
    with open("flag.txt") as f:
        print(f.read())
else:
    print("Hmm... not quite.")
