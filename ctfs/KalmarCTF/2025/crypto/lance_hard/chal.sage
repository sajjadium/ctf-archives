#!/usr/bin/env sage

from Crypto.PublicKey import ECC
from Crypto.Random import random as cryrand
from Crypto.Util.strxor import strxor
from hashlib import shake_128

samples = 1000

curve_bits = 80

p = (2^curve_bits).next_prime()
F = GF(p)
while True:
    a = F(cryrand.randrange(int(p)))
    b = F(cryrand.randrange(int(p)))
    E = EllipticCurve(F, [a,b])
    order = E.cardinality()
    if order.is_prime():
        break
print(p, a, b)

K = E.gens()[0] * cryrand.randrange(int(order))
r = cryrand.randrange(int(p))

for i in range(samples):
    a = cryrand.randrange(int(order))
    out = (a * K).x() + r
    print(a, out)

with open('flag.txt', 'r') as flag:
    flag = flag.read().strip().encode()
    keystream = shake_128(str((K.x(), r)).encode()).digest(len(flag))
    ctxt = strxor(keystream, flag)
    print(ctxt.hex())
