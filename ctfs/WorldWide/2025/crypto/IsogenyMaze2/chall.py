from sage.all import EllipticCurve, GF
from sage.all_cmdline import x
            
flag = "wwf{?????????????????????????????????????????????????????}"

p = 2**51 * 3**37 - 1
F = GF(p**2 , modulus=x**2 +1 , names=('i',)); (i,) = F._first_ngens(1)


def H(num, seed=0):
    j_prev = F(0)
    j = F(seed)
    while num:
        E = EllipticCurve(j = j)
        ns = []
        for m in E(0).division_points(2):
            ns.append(E.isogeny_codomain(m).j_invariant())
        ns = sorted(list(set(ns) - {j} - set(j_prev))) 
        j_prev = j
        j = ns[num % len(ns)]
        num //= len(ns)
    return j


import random
from Crypto.Util.number import bytes_to_long, long_to_bytes
from time import time

START = time()
rr = random.randbytes(16)
xx = bytes_to_long(rr)
hx = H(xx)
challenge = (xx, hx)
print(f'{challenge = }')
response = int(input("response: "))
if response == xx:
    exit()
if H(response) != hx:
    exit() 
if not all(0x20 <= i <= 0x7e for i in long_to_bytes(response)):
    exit()
if time() - START > 10:
    exit()
print(flag)