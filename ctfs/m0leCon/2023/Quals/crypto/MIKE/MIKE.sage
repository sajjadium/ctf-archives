import random
import hashlib
from flag import FLAG

N = 64

def find_poly():
    while True:
        n = random.randint(2, N - 1)
        d = gcd(N, n)
        m = n // d
        if m > 1 and not is_prime_power(m):
            return cyclotomic_polynomial(n)


def circulant_gen():
    h = 1
    R = QuotientRing(ZZ[x], x^N - 1)
    for i in range(100):
        f = find_poly()
        h = R(f * h)
    v = h.list()
    l = N - len(v)
    for i in range(l):
        v.append(0)
    M = matrix.circulant(v)
    return M


# public params
B = matrix.random(ZZ, nrows=N, ncols=N)
Q = B*B.transpose()
print(Q.list())

# key exchange
U1 = circulant_gen()
U2 = circulant_gen()

M1 = U1.transpose() * Q * U1
M2 = U2.transpose() * Q * U2

print(M1.list())
print(M2.list())

S1 = U1.transpose() * M2 * U1
S2 = U2.transpose() * M1 * U2

ss = hashlib.sha256(str(S1).encode()).digest()
enc = bytes([x^^y for x, y in zip(FLAG, ss)])
print(enc.hex())