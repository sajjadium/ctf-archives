from Crypto.Util.number import bytes_to_long
import random
from secret import flag
from functools import reduce
from random import randint
from gmpy2 import is_prime, next_prime, gcd, lcm

def gen_prime():
    while True:
        cnt = 0
        p = 1
        fs = []
        while cnt<4:
            e, x = randint(1,3), next_prime(randint(1, 2**128))
            p *= x**e
            cnt += e
            fs.append((x,e))
        if is_prime(2*p+1):
            fs.append((2,1))
            return 2*p+1, fs

def f1(a, p, fs):
    qs = [1]
    for t, e in fs:
        prev = qs[:]
        pn = 1
        for i in range(e):
            pn *= t
            qs.extend(a*pn for a in prev)
    qs.sort()

    for q in qs:
        if pow(a, q, p) == 1:
            return q

def f2(a, m, fs):
    assert gcd(a, m[0]*m[1]) == 1
    mofs = (f1(a, r, s) for r, s in zip(m, fs))
    return reduce(lcm, mofs, 1)

print("Generating data...")
p, pfs = gen_prime()
q, qfs = gen_prime()

assert p != q

n = int(p*q)
e = 65537
c = pow(bytes_to_long(flag), e, n)

print(f'{n = }')
print(f'{c = }')
print(f'{e = }')

for _ in range(10):
    g = int(input("Choose a value: "))
    assert g%n > 0
    M = int(f2(g, (p, q), (pfs, qfs)))
    print(f'{M = }')
