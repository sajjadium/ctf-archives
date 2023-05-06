#!/usr/bin/env sage
R = __import__('random').SystemRandom().randint

def gen_prime():
    while True:
        p = (ZZ^2).0
        while p.norm() < 5^55:
            a,b = ((-1)^R(0,1)*R(1,7^y) for y in (2,1))
            p *= matrix([[a,b],[123*b,-a]])
        p += (ZZ^2).0
        p *= diagonal_matrix((1,123)) * p
        if is_pseudoprime(p): return p

n = prod(gen_prime() for _ in 'yyyyyyy')
print(f'{n = :#x}')

m = int.from_bytes(open('flag.txt','rb').read().strip(), 'big')
c = int(pow(m, 1|2^2^2^2, n))
print(f'{c = :#x}')

