#!/usr/bin/env python3

from os import urandom
from Crypto.Util.number import getPrime as gp
from random import getrandbits, shuffle


random_int = lambda size: int(urandom(size).hex(), 16)

secret = b'FLAG'
secret = int(secret.hex(),16)

class shamir:
    def __init__(self, p, coeffs):
        self.p = p
        self.coeffs = coeffs
        
    def getshare(self, x, randfactor):
        result = 0
        for i, coeff in enumerate(self.coeffs):
            result = (result + coeff * pow(x, i)) % self.p
        return result + random_int(5)*randfactor

    def getshares(self,amount):
        factors = list(range(amount))
        shuffle(factors)
        x = random_int(5)
        ys = []
        factors = [self.getshare(x,i) for i in factors]
        return x, factors


p = gp(30)
print(f"Public Parameter: {p}")
coeffs = [secret] + [random_int(28) for i in range(4)]
poly = shamir(p, coeffs)

while True:
    opt = input('Share (yes/no) > ')
    if opt != 'yes':
        break
    amount = int(input('Amount > '))
    assert amount > 4
    res = poly.getshares(amount)
    print(res)
