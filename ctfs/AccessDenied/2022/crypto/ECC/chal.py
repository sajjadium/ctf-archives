import tinyec.ec as ec
import tinyec.registry as reg
from hashlib import sha256
from random import randint


class RNG:
    def __init__(self, seed):
        self.state = seed
    
    def next(self):
        self.state = self.state + 1
        return self.state

def hashInt(msg):
    h = sha256(msg).digest()
    return int.from_bytes(h, 'big')

def sign(msg):
    m = hashInt(msg)
    k = rand.next()
    R = k * G
    r = R.x
    s = pow(k, -1, n) * (m + r * d) % n
    return (r, s)
    
def verify(msg, sig):
    r, s = sig
    m = hashInt(msg)
    sinv = pow(s, -1, n)
    u1 = m * sinv % n
    u2 = r * sinv % n
    R_ = u1 * G + u2 * Q
    r_ = R_.x
    return r_ == r


C = reg.get_curve("secp256r1")
G = C.g
n = C.field.n
d =  int(open("flag.txt", "rb").read().hex(), 16)
Q = d * G

rand = RNG(randint(2, n-1))

# Let's sign some msgs

m1 = b"crypto means cryptography"
m2 = b"may the curve be with you"
m3 = b"the annoying fruit equation"

sig1 = sign(m1)
sig2 = sign(m2)
sig3 = sign(m3)

assert verify(m1, sig1)
assert verify(m2, sig2)
assert verify(m3, sig3)

open("out.txt", "w").write(f"{sig1 = }\n{sig2 = }\n{sig3 = }")
