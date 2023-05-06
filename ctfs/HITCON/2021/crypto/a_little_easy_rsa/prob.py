from Crypto.Util.number import *

N = 1024
P = 211
p = getPrime(P)
q = getPrime(N-P)
n = p*q
print(n.bit_length())
d = p
e = inverse(d, (p-1)*(q-1))
flag = bytes_to_long(open('flag','rb').read())

print(n)
print(e)
print(pow(flag, e, n))
