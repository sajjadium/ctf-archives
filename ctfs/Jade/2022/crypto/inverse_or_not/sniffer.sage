import random
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from secret import flag2 as flag

# new and improved
def Encrypt(pt, P, Q, G, n):
    s = random.randint(0, n)
    T = G ^ s
    E = T * P * T
    K = T * Q * T
    
    key = sum(K.list())
    key = long_to_bytes(ZZ(key))[:32]
    ct = AES.new(key, AES.MODE_ECB).encrypt(pad(pt, 32))
    return ct, E

# will it work?
def Decrypt(ct, E, R):
    L = R * E * R

    key = sum(L.list())
    key = long_to_bytes(ZZ(key))[:32]
    pt = AES.new(key, AES.MODE_ECB).decrypt(ct)
    return unpad(pt, 32)

# I hope you are not here, before allay?
# why bcoz, I am yet to arrive...
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p * q

M = MatrixSpace(Zmod(n), 2, 2)

while True:
    P = M.random_element()
    R = M.random_element()
    if P * R != R * P:
        break

# inverses waste cpu
r = random.randint(0, n)
G = R ^ r
Q = R * P * R

pt = flag
ct, E = Encrypt(pt, P, Q, G, n)
assert Decrypt(ct, E, R) == pt

pub  = {'n': n, 'P': P.list(), 'Q': Q.list(), 'G': G.list()}
priv = {'p': p, 'q': q, 'R': R.list()}

pub['ct'] = ct.hex()
pub['E'] = E.list()
print(pub)