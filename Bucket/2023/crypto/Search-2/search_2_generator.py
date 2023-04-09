from Crypto.Util.number import getPrime, inverse, bytes_to_long, isPrime
from string import ascii_letters, digits
from random import choice

p = bytes_to_long(open("flag.txt", "rb").read())
m = 0
while not isPrime(p):
    p += 1
    m += 1
q = getPrime(len(bin(p)))
n = p * q
e = 65537
l = (p-1)*(q-1)
d = inverse(e, l)

m = pow(m, e, n)
print(m)
print(n)
print(d)