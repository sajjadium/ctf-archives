from Crypto.Util.number import *
from gmpy2 import legendre

flag = bytes_to_long(open("flag.txt", "rb").read())

p, q = getPrime(256), getPrime(256)
n = p * q

x = getRandomRange(0, n)
while legendre(x, p) != -1 or legendre(x, q) != -1:
    x = getRandomRange(0, n)

def gm_encrypt(msg, n, x):
    y = getRandomRange(0, n)
    enc = []
    while msg:
        bit = msg & 1
        msg >>= 1
        enc.append((pow(y, 2) * pow(x, bit)) % n)
        y += getRandomRange(1, 2**48)
    return enc

print("n =", n)
print("x =", x)
print("enc =", gm_encrypt(flag, n, x))