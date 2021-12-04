from gmpy2 import next_prime, is_prime
from random import randint
from Crypto.Util.number import bytes_to_long

class Rand:
    def __init__(self):
        self.seed = randint(2, 2**512)
        self.A = next_prime(randint(2, 2**512))
        self.B = next_prime(randint(2, 2**512))
        self.M = next_prime(randint(2, 2**512))
        for _ in range(10000):
            self.next()
    
    def next(self):
        self.seed = self.seed * self.A + self.B
        self.seed = self.seed % self.M
        return self.seed

    def __str__(self):
        return f"{self.A}, {self.B}, {self.M}"
        

def gen_prime(r):
    while True:
        v = r.next()
        if is_prime(v):
            return v

r = Rand()
p,q = gen_prime(r), gen_prime(r)
n = p*q
e = 65537
flag = bytes_to_long(open('flag','rb').read())
val = pow(flag, e, n)

print(n)
print(r)
print(val)
