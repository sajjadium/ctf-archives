import random
from Crypto.Util.number import *
import gmpy2

class LCG:
    def __init__(self, a, c, m, seed):
        self.seed = seed
        self.multiplier = a
        self.increment = c
        self.modulus = m
    
    def next(self):
        self.seed = (self.multiplier*self.seed + self.increment) % self.modulus
        return self.seed
    
    def __str__(self):
        return ",".join(map(str, [self.seed, self.multiplier, self.increment, self.modulus]))

def gen_primes(PRIME_SIZE):
    lcg = LCG(random.getrandbits(PRIME_SIZE//4), random.getrandbits(PRIME_SIZE//4), random.getrandbits(PRIME_SIZE//4), random.getrandbits(PRIME_SIZE//4))    
    
    r1 = random.getrandbits(PRIME_SIZE//4)
    p = r1 << ((PRIME_SIZE*3)//4)
    for _ in range(3):
        p = p | (lcg.next() << (PRIME_SIZE*(2 - _))//4)
        
    r2 = random.getrandbits(PRIME_SIZE//4)
    q = r2 << ((PRIME_SIZE*3)//4)
    for _ in range(3):
        q = q | (lcg.next() << (PRIME_SIZE*(2 - _))//4)
        
    return lcg, p, q

while True:
    lcg, p, q = gen_primes(512)
    if gmpy2.is_prime(p) and gmpy2.is_prime(q) and gmpy2.gcd(lcg.multiplier, lcg.modulus) == 1:
        break

#print(lcg)
n = p * q
e = 65537
flag = b''
c = pow(bytes_to_long(flag), e, n)
print(f"n: {n}")
print(f"ct: {c}")
print("Hint:")
print([lcg.next() for _ in range(6)])