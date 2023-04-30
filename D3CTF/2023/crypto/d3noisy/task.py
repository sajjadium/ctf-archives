from Crypto.Util.number import *
from random import shuffle
from sympy import nextprime

def getKey():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    N = [getRandomNBitInteger(3211) for _ in range(15)]
    d = 0
    for _ in N:
        d = d ^ _
    d = nextprime(d)
    e = inverse(d,(p-1)*(q-1))
    return N, n, e

def leak(N):
    p,S = [],[]
    for i in range(15):
        p.append(getPrime(321))
        r = [N[_]%p[i] for _ in range(15)]
        shuffle(r)
        S.append(r)
    return p, S

m = bytes_to_long(flag)
N,n,e = getKey()
p,S = leak(N)
c = pow(m,e,n)

print(f"n = {n}")
print(f"p = {p}")
print(f"S = {S}")
print(f"c = {c}")

