import os
import signal
import random
from base64 import b64encode
from Crypto.Util.number import getStrongPrime, bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from flag import flag

p = getStrongPrime(1024)

key = os.urandom(32)
iv = os.urandom(AES.block_size)
aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
c = aes.encrypt(pad(flag, AES.block_size))

key = bytes_to_long(key)
print("Encrypted flag: {}".format(b64encode(iv + c).decode()))
print("p = {}".format(p))
print("key.bit_length() = {}".format(key.bit_length()))

signal.alarm(600)
while key > 0:
    r = random.randint(2, p-1)
    s = random.randint(2, p-1)
    t = random.randint(2, p-1)
    print("t = {}".format(t))

    a = int(input("a = ")) % p
    b = int(input("b = ")) % p
    c = int(input("c = ")) % p
    d = int(input("d = ")) % p
    assert all([a > 1 , b > 1 , c > 1 , d > 1])
    assert len(set([a,b,c,d])) == 4

    u = pow(a, r, p) * pow(c, s, p) % p
    v = pow(b, r, p) * pow(c, s, p) % p
    x = u ^ (key & 1)
    y = v ^ ((key >> 1) & 1)
    z = pow(d, r, p) * pow(t, s, p) % p

    key = key >> 2

    print("x = {}".format(x))
    print("y = {}".format(y))
    print("z = {}".format(z))
