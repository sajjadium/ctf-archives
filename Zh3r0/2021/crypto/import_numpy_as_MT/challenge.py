import os
from numpy import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secret import flag

def rand_32():
    return int.from_bytes(os.urandom(4),'big')

flag = pad(flag,16)

for _ in range(2):
    # hate to do it twice, but i dont want people bruteforcing it
    random.seed(rand_32())
    iv,key = random.bytes(16), random.bytes(16)
    cipher = AES.new(key,iv=iv,mode=AES.MODE_CBC)
    flag = iv+cipher.encrypt(flag)


print(flag.hex())

