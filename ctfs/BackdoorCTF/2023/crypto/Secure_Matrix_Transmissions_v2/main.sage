from sage.all import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import os
import hashlib
from base64 import b64encode, b64decode

FLAG = b'flag{REDACTED}' ## removed the flag

f = open('./intercepted.txt', 'w')

p = 33184772290615481426295675425316668758122179640330548849957081783509
N = 6
gl = GL(N, GF(p))

def encrypt(flag, shared_secret):
    i = 0
    key = 0
    for row in shared_secret:
        for item in row:
            key += item ** i
            i += 1

    key = hashlib.sha256(long_to_bytes(int(key))).digest()
    iv = os.urandom(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_text = cipher.encrypt(pad(flag, AES.block_size))

    return b64encode(iv + encrypted_text).decode("utf-8")

def decrypt(cipher, shared_secret):
    iv, enc = b64decode(cipher)[:16], b64decode(cipher)[16:]
    i = 0
    key = 0
    for row in shared_secret:
        for item in row:
            key += item**i
            i += 1

    key = hashlib.sha256(long_to_bytes(int(key))).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)

    flag = cipher.decrypt(enc)
    return unpad(flag, AES.block_size)

def gen_params():
    
    a = matrix(gl.random_element())
    b = matrix(gl.random_element())
    w = matrix(gl.random_element())

    while a.det() == 0 or b.det() == 0 or w.det() == 0:
        a = matrix(gl.random_element())
        b = matrix(gl.random_element())
        w = matrix(gl.random_element())

    f.write(f"a = \n{a}\n")   ## intercepted successfully!  
    f.write(f"b = \n{b}\n")   ## intercepted successfully!
    f.write(f"w = \n{w}\n")   ## intercepted successfully!

    return a, b, w

## generate public parameters
a, b, w = gen_params()

## for Alice
n = random.randint(p // 4, p // 2)
m = random.randint(p // 4, p // 2)

## Sends to Bob
u = a ** n * w * b ** m
f.write(f"u = \n{u}\n")   ## intercepted successfully!

## for Bob
r = random.randint(p // 4, p // 2)
s = random.randint(p // 4, p // 2)

## Sends to Alice
v = a ** r * w * b ** s
f.write(f"v = \n{v}\n")   ## intercepted successfully!

Ka = a ** n * v * b ** m
Kb = a ** r * u * b ** s

## Sends to Bob
ct1 = encrypt(b'send me the new flag please', Ka)  
f.write(f"ct1 = {ct1}\n")   ## intercepted successfully!

f.write(f"{decrypt(ct1, Kb).decode()}\n")

## Sends to Alice
ct2 = encrypt(FLAG, Kb)
f.write(f"ct2 = {ct2}\n")   ## intercepted successfully!

## Read the Flag
# f.write(decrypt(ct2, Ka).decode())
