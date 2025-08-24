from Crypto.Util.number import bytes_to_long as btl, long_to_bytes as ltb
from random import random
import os
key = b"LITCTF{[redacted]}"
keyLen = len(key)
keyInt = btl(key)

def getRand():
        copy = keyInt
        res = ""
        for _ in range(keyLen*8):
                bit = copy % 2
                copy >>= 1
                add = int(random() / random() + 0.5) % 2
                res += str(bit ^ add)
        res = res[::-1]
        return res

for _ in range(1000):
        print(getRand())

print(ltb(int(getRand(), 2) ^ btl(key)).hex())