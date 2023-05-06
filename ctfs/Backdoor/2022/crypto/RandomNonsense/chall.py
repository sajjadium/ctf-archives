#!/usr/bin/python
from Crypto.Util.number import long_to_bytes, bytes_to_long
from math import gcd
import ecdsa
import random
import hashlib
import string

Curve = ecdsa.NIST384p
G = Curve.generator
n = Curve.order

counter = 7
flag = 'REDACTED'
msg_to_sign = b'''Sign me to get the flag'''
KEYS = string.ascii_letters + string.digits
VALUES = range(1, len(KEYS) + 1)
MAP = dict(zip(KEYS, VALUES))

def encode(m: bytes) -> int:
    m = m.decode()
    enc_arr = range(1, counter + 1)
    if len(list(set(m))) == counter:
        s = set()
        enc_arr = []
        for x in m:
            if x in s:
                continue
            enc_arr.append(MAP[x])
            s.add(x)
    return sum([(-2)**i*x for i, x in enumerate(enc_arr)])%n

def gen_keypair():
    d = random.randint(1, n-1)
    Q = d*G
    return d, Q

def inv(z: int):
    return pow(z, -1, n)

def sign(msg, d):
    x = int(hashlib.sha256(long_to_bytes(encode(msg) & random.randrange(1, n - 1))).hexdigest(), 16) % 2**50
    while True:
        k = (random.getrandbits(320) << 50) + x
        r = (k*G).x()
        if r != 0:
            break

    m = int(hashlib.sha256(msg).hexdigest(), 16)
    s = (inv(k)*(m + r*d)) % n
    return (int(r), int(s)) 

def verify(msg, r, s):
    z = int(hashlib.sha256(msg).hexdigest(), 16)
    VV = z*inv(s)*G + r*inv(s)*Q
    if (VV.x() - r)%n == 0:
        return True
    return False

d, Q = gen_keypair()

def main():
    global counter
    options = '''Here are your options:
    [S]ign a message
    [V]erify a signature
    [P]ublic Key
    [Q]uit'''

    print(options)
    choice = input('choice? ')
    choice = choice.lower()

    if choice == 'p':
        print(Q.x(), Q.y(), n)

    if choice == 'v':
        msg = input('msg? ').encode()
        r = int(input('r? '))
        s = int(input('s? '))
        if verify(msg, r, s):
            print('Successful Verification')
            if msg == msg_to_sign:
                print(f'Flag: {flag}')
        else:
            print('Try Again !')
    if choice == 's':
        msg = input('msg? ').encode()
        r, s = sign(msg, d)
        if msg != msg_to_sign:
            print(f'r={r}, s={s}')

    if choice == 'q':
        exit(0)
    counter += 1

d, Q = gen_keypair()
print('Welcome to my secure signature scheme !!')

if __name__ == '__main__':
    for _ in range(50):
        main()
