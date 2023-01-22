from Crypto.Util.number import *
from secret import flag
from hashlib import sha256

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

E = EllipticCurve(GF(p), [a,b])
G = E.gens()[0]
q = G.order()
priv = Integer(bytes_to_long(flag))

def sign(msg, d):
    k = int.from_bytes(sha256(int(d).to_bytes(d.nbits()//8 + 1, 'big') + sha256(msg).digest()).digest(), 'big')
    z = int.from_bytes(sha256(msg).digest(),'big')
    r = int((k * G)[0]) % q
    s = (inverse_mod(k, q) * (z + d * r)) % q
    leak_k = (k >> 120) << 120
    return z, r, s, leak_k

for i in range(2):
    msg = input("Enter message: ").encode()
    print(sign(msg, priv))
