from Crypto.Util.number import *
from math import prod
from secret import flag

def keygen(pbits,kbits,k):
    p = getPrime(pbits)
    x = [getPrime(kbits + 1) for i in range(k)]
    y = prod(x)
    while 1:
        r = getPrime(pbits - kbits * k)
        q = 2 * y * r + 1
        if isPrime(q):
            return p*q, (p, q, r, x)

def encrypt(key, message):
    return pow(0x10001, message, key)

key = keygen(512, 24, 20)
flag = bytes_to_long(flag)
messages = [getPrime(flag.bit_length()) for i in range(47)] + [flag]
enc = [encrypt(key[0], message) for message in messages]

print(messages[:-1])
print(enc)
