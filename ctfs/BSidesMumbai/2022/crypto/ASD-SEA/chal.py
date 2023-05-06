from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from Crypto.PublicKey import DSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA
import os


def sign(msg):
    h = SHA.new(msg).digest()
    n = bytes_to_long(h + os.urandom(2))

    assert 1 < n < key.q-1

    r = pow(key.g,n,key.p) % key.q
    s = inverse(n, key.q)*(bytes_to_long(h) + key.x*r) % key.q
    return s, r

def verify(msg, s, r):
    h = bytes_to_long(SHA.new(msg).digest())
    w = inverse(s, key.q)
    u1 = h*w % key.q
    u2 = r*w % key.q
    v = (pow(key.g,u1,key.p)*pow(key.y,u2,key.p) %key.p) % key.q
    return v==r


FLAG = open('flag.txt', 'rb').read()

key = DSA.generate(2048)
open("pubkey.pem", "wb").write(key.publickey().export_key())

m = open('msg.txt', 'rb').read()
s, r = sign(m)
isVerified = verify(m,s,r)

print("Signature: (", s, ",", r, ")")
print("Verification Status:", isVerified)

if isVerified:
    aesKey = pad(long_to_bytes(key.x), 16)
    cipher = AES.new(aesKey, AES.MODE_ECB).encrypt(pad(FLAG,16)).hex()
    print("Cipher:", cipher)
