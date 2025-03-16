import random
from Crypto.PublicKey import RSA
from Crypto.Util.number import *

def nextPrime(prim):
    if isPrime(prim):
        return prim
    else:
        return nextPrime(prim+1)

p = getPrime(512)
q = nextPrime(p+1)
while p%4 != 3 or q%4 !=3:
    p = getPrime(512)
    q = nextPrime(p+1)

n = p*q
m = bytes_to_long( open('flag.txt','rb').read() )

c = pow(m, e, n)

rsa = RSA.construct((n, e))
print(rsa.exportKey().decode())
print(f"cipher: { long_to_bytes(c) }")