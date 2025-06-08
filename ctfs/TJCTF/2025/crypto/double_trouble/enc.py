from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random

def gen():
    myrandom = random.Random(42)
    k1 = myrandom.randbytes(8)
    choices = list(myrandom.randbytes(6))
    k2 = b''
    for _ in range(8):
        k2 += bytes([choices[random.randint(0, 3)]])
    return k1, k2

def enc(data, k1, k2,  k3, k4):
    key1 = k1+k2
    cipher = AES.new(key1, mode=AES.MODE_ECB)
    ct1 = cipher.encrypt(pad(data, 16))
    key2 = k4+k3
    cipher = AES.new(key2, mode=AES.MODE_ECB)
    ct2 = cipher.encrypt(ct1)
    return ct2

k1, k2 = gen()
k3, k4 = gen()

pt = b"example"

with open('flag.txt') as f:
    flag = f.read().encode()

with open('out.txt', "w") as f:
    f.write(enc(pt, k1, k2, k3, k4).hex())
    f.write("\n")
    f.write(enc(flag, k1, k2, k3, k4).hex())