from json import dump as json_dump
from random import randint
from mpmath import mp
from Crypto.Util.number import bytes_to_long, getPrime, GCD


size = 768//8


def pad(data, length):
    if len(data) >= length:
        raise ValueError("length of data is too large.")
    pad_data = bytes([randint(1, 255) for _ in range(length - len(data) - 1)])
    return pad_data + b'\x00' + data


mp.dps = 8*size*16

p = getPrime(8*size)
q = getPrime(8*size)
e = 3
while GCD(q-1, e) != 1 or GCD(p-1, e) != 1:
    p = getPrime(8*size)
    q = getPrime(8*size)

if p > q:
    p, q = q, p

p_n = mp.fdiv(mp.mpf(str(1)), mp.mpf(p))
q_n = mp.mpf(q)
n = mp.fmul(p_n, q_n)

flag = open("flag.txt","rb").read().strip()
flag = bytes_to_long(pad(flag, size-1))

ciphertext = pow(flag, e) % n

json_dump(
    {
        'n': str(n),
        'e': str(e),
        'c': str(ciphertext),
    },
    open('output.txt', 'w')
)
