#!/usr/bin/python
from sage.all import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import os
import hashlib
from base64 import b64encode, b64decode
p = 100458505468885003633418577656224333902553170484436983273607309963845847739507115860865964753239939027972338834707903941940188314348678981808910413754306718965087266944429878241410578991733762502442817585765598816431431108282071433256273345939973526837788093199292557721204590554061504359121574222368307048919809010489980961017706729222034791017130925070426893349814057145812995340991548906078333104951440614482037356443864699967124299012034397810342312642333550598174454039699165710636052240583294703998189114479917657125270697086234200442489544474659560583354052797579309573507121265302226528942789519
n = 4

def gen_random_matrix():
    return matrix(GF(p), n, [random.randint(0, p) for _ in range(n*n)])

M = gen_random_matrix()

def gen_matrix_singular():
    while True:
        S = gen_random_matrix()
        while S.det() == 0:
            S = gen_random_matrix()
        entries = [random.randint(0, p) for _ in range(n - 1)] + [0]
        D = diagonal_matrix(GF(p), entries)
        H = S.inverse()*D*S
        if M*H != H*M:
            return H

def multiply(M, H1i, H2i, M_, H1j, H2j):
    return (H1j*M*H2j + M_, H1i*H1j, H2i*H2j)

def power(M, H1, H2, m):
    res = (O, I, I)
    x = (M, H1, H2)

    while m != 0:
        if m & 1:
            lt = [*res, *x]
            res = multiply(*res, *x)
        x = multiply(*x, *x)        
        m = m >> 1
    return res

def encrypt(flag, shared_secret):
    i = 0
    key = 0
    for row in shared_secret:
        for item in row:
            key += item**i
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

H1 = gen_matrix_singular()
H2 = gen_matrix_singular()
I = identity_matrix(GF(p), n)
O = zero_matrix(GF(p), n)

flag = b'flag{REDACTED}'
x, y = random.randint(1, p - 1), random.randint(1, p - 1)
A, B = power(M, H1, H2, x), power(M, H1, H2, y)
assert multiply(*A, *B)[0] == multiply(*B, *A)[0]
shared_secret = multiply(*A, *B)[0]
cip = encrypt(flag, shared_secret)
decrypted = decrypt(cip, shared_secret)
assert decrypted == flag

f = open('enc.txt', 'w')
print(f"p={p}", file=f)
print(f"n={n}", file=f)
print(f"M={list(M)}", file=f)
print(f"H1={list(H1)}", file=f)
print(f"H2={list(H2)}", file=f)
print(f"A={list(A[0])}", file=f)
print(f"B={list(B[0])}", file=f)
print(f"cip={cip}", file=f)
