from math import log, e, pi
from secrets import randbelow
from secret import FLAG
from gmpy2 import is_prime

delta = lambda k, n : 1/(2*k+1) + \
                      log(2*k**3)/(2*(2*k+1)*log(n)) + \
                      (log(2*k+1) - log(2*pi*e) - log(4*k**3))/(4*log(n))

def getPrime(pbits, M, k=8):

    assert M.bit_length() < pbits//k, "M is too big"

    ub = delta(k, 2**(2*pbits)-1)
    a = randbelow(100)

    p = 0
    for i in range(k+1):
        x = randbelow(2**(pbits - (M**k).bit_length()) - a.bit_length()) * a
        while x.bit_length() / (pbits*2) >= ub:
            x = randbelow(2**(pbits - (M**k).bit_length()) - a.bit_length()) * a
        
        p += x*M**i

    while not is_prime(p//a):
        p -= a
    
    return p//a

M = 2**122

e = 0x10001
p = getPrime(1024, M)
q = getPrime(1024, M)
N = p * q

pt = int.from_bytes(FLAG, 'big')
ct = pow(pt, e, N)

with open('enc', 'w') as f:
    print(f'{e = }', file=f)
    print(f'{N = }', file=f)
    print(f'{ct = }', file=f)