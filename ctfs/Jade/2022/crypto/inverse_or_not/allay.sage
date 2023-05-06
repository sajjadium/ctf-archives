import random
from Crypto.Util.number import *
from secret import flag1 as flag

# not copied, duh!
def encrypt(pt, P, Q, G, n):
    s = random.randint(0, n)
    T = G ^ s
    E = ~T * P * T
    K = ~T * Q * T
    ct = K * pt * K
    return ct, E

def decrypt(ct, E, R):
    L = ~R * E * R
    pt = L * ct * L
    return pt


# everything needs to be strong
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p * q

# Love for Matrices
M = MatrixSpace(Zmod(n), 2, 2)

while True:
    P = M.random_element()
    R = M.random_element()
    if P * R != R * P:
        break

# inverse sorcery
r = random.randint(0, n)
G = R ^ r
Q = ~R * ~P * R

h = round(len(flag) / 4)
pt = [bytes_to_long(flag[i: i + h]) for i in range(0, len(flag), h)]
pt = M(pt)
ct, E = encrypt(pt, P, Q, G, n)
assert decrypt(ct, E, R) == pt

pub  = {'n': n, 'P': P.list(), 'Q': Q.list(), 'G': G.list()}
priv = {'p': p, 'q': q, 'R': R.list()}

pub['ct'] = ct.list()
pub['E'] = E.list()
print(pub)