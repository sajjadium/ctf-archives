from Crypto.Util.number import *
from flag import flag


def magic2(a):
    sum = 0
    for i in range(a):
        sum += i * 2 + 1
    return sum


def magic(p, q, r):
    x = p + q
    for i in range(3):
        x = magic2(x)
    return x % r


m = bytes_to_long(flag.encode())
p = getPrime(512)
q = getPrime(512)
r = getPrime(1024)
n = p * q
e = 65537
c = pow(m, e, n)
s = magic(p, q, r)
print("r:", r)
print("n:", n)
print("e:", e)
print("c:", c)
print("s:", s)
