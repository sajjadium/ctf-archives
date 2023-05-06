from Crypto.Cipher import AES
from hashlib import sha256
from Crypto.Util.number import getPrime, inverse
from Crypto.Util.Padding import pad, unpad
import random
from time import time
import os

from tonelli_shanks import tonelli_shanks

from collections import namedtuple
Point = namedtuple("Point", "x y")
O = 'Origin'

def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)

def point_addition(P: tuple, Q: tuple):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:  # approx. time around 30µs when entering else's segment
        if P == Q:
            aux = ((3*P.x**2 + a) * inverse(2*P.y, p))%p
        else:
            aux = ((Q.y - P.y) * inverse((Q.x - P.x), p))%p
    Rx = (aux**2 - P.x - Q.x) % p
    Ry = (aux*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    return R

def double_and_add(P: tuple, n: int):
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    return R

FLAG = b"[REDACTED]" 

p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
G = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

# Leonard's public key
leonard_public_key = 31663442885885219669071274428005652588471134165143253841118506078548146970109
leonard_public_point = Point(leonard_public_key, tonelli_shanks((leonard_public_key**3 + a*leonard_public_key + b)%p,p)[0])

# My private key
my_private_key = random.randint(2**(243),2**244-1)

# My public key:
my_public_key = double_and_add(G, my_private_key).x
print(my_public_key)

# Our shared private key:
begin = time()
shared_secret_key = double_and_add(leonard_public_point, my_private_key).x
for k in range(999999) : # I want to be precise on the computing time, i've even gave you the time it takes to run the function above!
    double_and_add(leonard_public_point, my_private_key)
computing_time = (time() - begin)
print("You can be proud I can compute my message in less than {}microsec".format(computing_time))

# Encryption of my message
derived_aes_key = sha256(str(shared_secret_key).encode('ascii')).digest()
iv = os.urandom(16)
cipher = AES.new(derived_aes_key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(FLAG,16,'pkcs7'))
print(iv.hex())
print(ciphertext.hex())
