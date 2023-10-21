import hashlib
import ecdsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from secret import flag

def gen():
    curve = ecdsa.NIST256p.generator
    order = curve.order()
    d = randint(1, order-1)
    while d.bit_length() != 256:
        d = randint(1, order-1)
    pubkey = ecdsa.ecdsa.Public_key(curve, curve * d)
    privkey = ecdsa.ecdsa.Private_key(pubkey, d)
    return pubkey, privkey, d

def nonce_gen(msg, d):
    msg_bin = bin(msg)[2:].zfill(256)
    d_bin = bin(d)[2:].zfill(256)
    nonce = int(msg_bin[:128] + d_bin[:128], 2)
    return nonce

def sign(msg, privkey, d):
    msg_hash = bytes_to_long(hashlib.sha256(msg).digest())
    nonce = nonce_gen(msg_hash, d)
    sig = privkey.sign(msg_hash, nonce)
    s, r = sig.s, sig.r
    return s, r

pk, sk, d = gen()
msg = b'welcome to n1ctf2023!'
s, r = sign(msg, sk, d)
print(f's = {s}')
print(f'r = {r}')

m = pad(flag, 16)
aes = AES.new(long_to_bytes(d), mode=AES.MODE_ECB)
cipher = aes.encrypt(m)
print(f'cipher = {cipher}')

"""
s = 98064531907276862129345013436610988187051831712632166876574510656675679745081
r = 9821122129422509893435671316433203251343263825232865092134497361752993786340
cipher = b'\xf3#\xff\x17\xdf\xbb\xc0\xc6v\x1bg\xc7\x8a6\xf2\xdf~\x12\xd8]\xc5\x02Ot\x99\x9f\xf7\xf3\x98\xbc\x045\x08\xfb\xce1@e\xbcg[I\xd1\xbf\xf8\xea\n-'
"""