import hashlib
import random
from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from ecdsa import NIST256p

from flag import FLAG

message = b"ECDSA prevents forging messages"

curve = NIST256p
G = curve.generator
n = curve.order

class Signature:
    def __init__(self):
        self.privkey = random.randrange(n)
        self.pubkey = self.privkey * G
        self.r = random.randrange(n)
        self.s = random.randrange(n)

    def sign(self, msg, k):
        hsh = int(hashlib.sha256(msg).hexdigest(), 16)
        p = k * G
        self.r = p.x() % n
        self.s = (inverse(k, n) * (hsh + (self.privkey * self.r) % n)) % n
        return (self.r, self.s)

    def f_sign(self, msg, k):
        hsh = int(hashlib.sha256(msg).hexdigest(), 16)
        self.s = (inverse(k, n) * (hsh + (self.privkey * self.r) % n)) % n
        return (self.r, self.s)

sig = Signature()
k = random.randrange(n)

sig1 = sig.sign(message, k)
sig2 = sig.f_sign(message, k^0xffffffff)
sig3 = sig.f_sign(message, k^0xffffffff00000000)

r = random.randrange(n)
pubkey2 = r*G
sharedkey = r*sig.pubkey

iv = get_random_bytes(16)
key = long_to_bytes(int(sharedkey.x()))
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(FLAG, 16))

print("pubkey="+ str((int(sig.pubkey.x()), int(sig.pubkey.y()))))
print("sig1=" + str(tuple(map(lambda x:int(x), sig1))))
print("sig2=" + str(tuple(map(lambda x:int(x), sig2))))
print("sig3=" + str(tuple(map(lambda x:int(x), sig3))))

print("pubkey2="+ str((int(pubkey2.x()), int(pubkey2.y()))))
print("iv=" + "0x"+str(iv.hex()))
print("ct=" + "0x"+str(ct.hex()))
