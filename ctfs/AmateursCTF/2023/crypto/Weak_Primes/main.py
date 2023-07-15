from Crypto.Util.number import *
from flag import flag


def phi(p, q):
    if p == q:
        return (p-1)*p
    else:
        return (p-1)*(q-1)


def getModPrime(modulus):
    p = 2**2047 + getPrime(128)
    p += (modulus - p) % modulus
    p += 1
    iters = 0
    while not isPrime(p):
        p += modulus
    return p


flag = bytes_to_long(flag)
p = getPrime(2048)
q = getModPrime(3)

n = p*q
e = 65537
d = inverse(e, phi(p, q))
c = pow(flag, e, n)

with open('output.txt', 'w') as f:
    f.write(f"{c} {e} {n}")
