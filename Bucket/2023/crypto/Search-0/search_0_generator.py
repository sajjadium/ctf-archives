from Crypto.Util.number import getPrime, inverse, bytes_to_long
from string import ascii_letters, digits
from random import choice

m = open("flag.txt", "rb").read()
p = getPrime(128)
q = getPrime(128)
n = p * q
e = 65537
l = (p-1)*(q-1)
d = inverse(e, l)

m = pow(bytes_to_long(m), e, n)
print(m)
print(n)

p = "{0:b}".format(p)
for i in range(0,108):
    print(p[i], end="")