import random
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256
import os

N = 100000
flag = b'wxmctf{REDACTED}'

f = open("out.txt", "w")

def compose(a, b):
    r = []
    for i in range(N):
        r.append(b[a[i]])
    return r

G = [x for x in range(N)]
random.shuffle(G)
print(G,file=f)

def mult(p, c):
    if c == 0:
        return [x for x in range(N)]
    elif not c%2:
        return mult(compose(p, p), c>>1)
    else:
        return compose(p, mult(compose(p, p), c>>1))


    
a = bytes_to_long(os.urandom(40))
b = bytes_to_long(os.urandom(40))

A = mult(G, a)
B = mult(G, b)

print(A,file=f)
print(B,file=f)

s = mult(A, b)

assert s == mult(B, a)
iv = os.urandom(16)
aes = AES.new(sha256(str(s).encode()).digest()[:16], AES.MODE_CBC, iv=iv)
print(iv.hex(),file=f)
print(aes.encrypt(flag).hex(),file=f)

f.close()
