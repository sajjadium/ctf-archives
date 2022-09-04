from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import random
from hashlib import sha256
from secret import FLAG

class ShareScheme:
    def __init__(self, key: bytes):
        assert len(key) == 128
        self.key1 = bytes_to_long(key[:64])
        self.key2 = bytes_to_long(key[64:])

    def getShare(self):
        p = getPrime(512)
        a = random.randint(2, p - 1)
        b = random.randint(2, p - 1)
        c = random.randint(2, p - 1)
        y = (a + self.key1 * b + self.key2 * c) % p
        return p, a, b, c, y
        
def commit(val: int):
    p = getPrime(512)
    g = random.randint(2, p - 1)
    print(f"Commitment: {p} {g} {pow(g, val, p)}")

key = os.urandom(128)
ss = ShareScheme(key)

real_key = sha256(key).digest()[:16]
cipher = AES.new(real_key, AES.MODE_ECB)
enc_flag = cipher.encrypt(pad(FLAG, 16))
print(f"flag = {enc_flag.hex()}")

while True:
    op = int(input("Option: "))
    if op == 1:
        p, a, b, c, y = ss.getShare()
        print(f"{p = }")
        print(f"{a = }")
        print(f"{b = }")
        print(f"{c = }")
        commit(y)
    else:
        exit(0)