from secret import flag
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

PRIMESIZE = 512
e = 65537

p = getPrime(PRIMESIZE)
q = getPrime(PRIMESIZE)
n = p*q
c = bytes_to_long(flag)
ct = pow(c,e,n)
msb = bin(p >> 20)[2:]
print(ct)
print(n)
print(msb)