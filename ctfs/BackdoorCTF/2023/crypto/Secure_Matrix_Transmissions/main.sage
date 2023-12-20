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

secret = matrix(gl.random_element())
secret_inv = secret ** (-1)

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

def secure_key_gen():
    temp = zero_matrix(GF(p), N)
    for i in range(N):
        temp[i, i] = random.randint(1, p - 1)
    return temp

def gen_params():
    
    A = matrix(gl.random_element())
    B = matrix(gl.random_element())

    while A.det() == 0 or B.det() == 0:
        A = matrix(gl.random_element())
        B = matrix(gl.random_element())

    f.write(f"A = \n{A}\n")   ## intercepted successfully!  
    f.write(f"B = \n{B}\n")   ## intercepted successfully!

    return A, B

## generate public parameters
A, B = gen_params()

## for Alice
a = secure_key_gen()

## Sends to Bob
u = secret_inv * A * secret * a * secret_inv * A ** (-1) * secret
f.write(f"u = \n{u}\n")   ## intercepted successfully!


## for Bob
b = secure_key_gen()
a_ = secret_inv * A ** (-1) * secret * u * secret_inv * A * secret
key_b = a_ + b

## Sends to Alice
v = secret_inv * B * secret * b * secret_inv * B ** (-1) * secret
f.write(f"v = \n{v}\n")   ## intercepted successfully!

## for Alice
b_ = secret_inv * B ** (-1) * secret * v * secret_inv * B * secret
key_a = b_ + a

## Sends to Bob
ct1 = encrypt(b'send me the flag', key_a)  
f.write(f"ct1 = {ct1}\n")   ## intercepted successfully!

## for Bob
f.write(f"{decrypt(ct1, key_b).decode()}\n")

## Sends to Alice
ct2 = encrypt(FLAG, key_b)
f.write(f"ct2 = {ct2}\n")   ## intercepted successfully!

## Read the Flag
# f.write(decrypt(ct2, key_a).decode())
