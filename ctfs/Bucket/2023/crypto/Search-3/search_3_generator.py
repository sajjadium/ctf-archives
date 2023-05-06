from Crypto.Util.number import getPrime, inverse, bytes_to_long, isPrime
from string import ascii_letters, digits
from random import choice


m = bytes_to_long(open("flag.txt", "rb").read())
p = getPrime(128)
q = getPrime(128)
n = p * p
e = 65537
l = (p-1)*(p-1)
d = inverse(e, l)

m = pow(m, e, n)
print(m)
print(n)