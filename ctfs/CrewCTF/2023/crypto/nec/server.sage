# secret import
from flag import FLAG

# secret import (genparam is defined)
from secret import genparam

import random
from os import urandom as os_urandom
from hashlib import sha512
from Crypto.Util.number import *


rbitsize = 900

def pr(s):
    print(s, flush=True)


def pad(data, length):
    if len(data) >= length:
        raise ValueError("length of data is too large.")
    pad_data = bytes([random.randint(1, 255) for _ in range(length - len(data) - 1)])
    return pad_data + b'\x00' + data


def gengenerator(E, h, r):
    # generator from random point
    while True:
        A = E.random_point()
        G = h * A
        if G != E([0, 1, 0]):
            break
    assert r * G == E([0, 1, 0])
    return G


def sign(msg, privkey, pubkey, nonceseedbytes):
    d = privkey
    r, G, P = pubkey
    hashval = sha512(msg).digest()
    nonce = sha512(nonceseedbytes + hashval).digest()
    hashvalint = int.from_bytes(hashval, 'big')
    nonceint = int.from_bytes(nonce, 'big')
    sig1 = int((nonceint * G)[0]) % r
    sig2 = (pow(nonceint, -1, r) * (hashvalint + d * sig1)) % r
    return int(sig1), int(sig2)


pr("generating EC parameters...")
r, q, h, ord, EC = genparam(rbitsize)
pr(f"bitsize of r: {int(r).bit_length()}")
pr(f"bitsize of q: {int(q).bit_length()}")
pr(f"bitsize of h: {int(h).bit_length()}")
assert EC.base_field().characteristic() == q
assert isPrime(r) and isPrime(q)
# ord = EC.order()
assert ord == h * r
assert abs(q - h*r) < 2**(rbitsize//2 + 8) 


privkey = getRandomInteger(rbitsize)
nonceseedbytes = os_urandom(rbitsize//8)


rrr = getPrime(rbitsize//2)
N = q * rrr
e = 0x10001
Nbytesize = int(N).bit_length()//8
m = int.from_bytes(pad(FLAG, Nbytesize - 1), 'big')
c = pow(m, e, N)

pr(f"N={hex(N)}")
pr(f"e={hex(e)}")
pr(f"c={hex(c)}")


for _ in range(4):
    G = gengenerator(EC, h, r)
    P = privkey * G
    pubkey = (r, G, P)
    try:
        msg_hex = input("input message (hex): ")
        msg = bytes.fromhex(msg_hex)
    except:
        pr("error occured")
        exit(0)
    sig1, sig2  = sign(msg, privkey, pubkey, nonceseedbytes)
    pr(f"signature: ({hex(sig1)}, {hex(sig2)})")

pr("Bye!")
