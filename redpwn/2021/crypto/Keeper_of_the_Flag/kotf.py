#!/usr/local/bin/python3

from Crypto.Util.number import *
from Crypto.PublicKey import DSA
from random import *
from hashlib import sha1

rot = randint(2, 2 ** 160 - 1)
chop = getPrime(159)

def H(s):
    x = bytes_to_long(sha1(s).digest())
    return pow(x, rot, chop)


L, N = 1024, 160
dsakey = DSA.generate(1024)
p = dsakey.p
q = dsakey.q
h = randint(2, p - 2)
g = pow(h, (p - 1) // q, p)
if g == 1:
    print("oops")
    exit(1)

print(p)
print(q)
print(g)

x = randint(1, q - 1)
y = pow(g, x, p)

print(y)


def verify(r, s, m):
    if not (0 < r and r < q and 0 < s and s < q):
        return False
    w = pow(s, q - 2, q)
    u1 = (H(m) * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return v == r


pad = randint(1, 2 ** 160)
signed = []
for i in range(2):
    print("what would you like me to sign? in hex, please")
    m = bytes.fromhex(input())
    if m == b'give flag' or m == b'give me all your money':
        print("haha nice try...")
        exit()
    if m in signed:
        print("i already signed that!")
        exit()
    signed.append(m)
    k = (H(m) + pad + i) % q
    if k < 1:
        exit()
    r = pow(g, k, p) % q
    if r == 0:
        exit()
    s = (pow(k, q - 2, q) * (H(m) + x * r)) % q
    if s == 0:
        exit()
    print(H(m))
    print(r)
    print(s)

print("ok im done for now")
print("you visit the flag keeper...")
print("for flag, you must bring me signed message:")
print("'give flag':" + str(H(b"give flag")))

r1 = int(input())
s1 = int(input())
if verify(r1, s1, b"give flag"):
    print(open("flag.txt").readline())
else:
    print("sorry")
