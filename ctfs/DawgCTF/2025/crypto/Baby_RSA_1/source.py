from Crypto.Util.number import *
from sage.all import randint

p = getPrime(512)
q = getPrime(512)
N = p * q

e = 0x10001

m = bytes_to_long(b"DawgCTF{fake_flag}")

c = pow(m, e, N)

print("N =", N)
print("e =", e)
print("ct =", c)
print()

a = randint(0, 2**100)
b = randint(0, 2**100)
c = randint(0, 2**100)
d = randint(0, 2**100)

x = a * p + b * q
y = c * p + d * q

print("a =", a)
print("b =", b)
print("c =", c)
print("d =", d)
print()
print("x =", x)
print("y =", y)





