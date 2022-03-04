from Crypto.Util.number import *

flag = b"GLUG{**********REDACTED***************}"

p,q = getPrime(1024),getPrime(1024)
N = p * p * q
e = 0x10001
phi = p * (p-1) * (q-1)

d = inverse(e, phi)
m = bytes_to_long(flag)
c = pow(m, e, N)
x = (p * q) % 2**1337

print("N =  {}".format(N))
print("e =  {}".format(e))
print("c = {}".format(c))
print("x =  {}".format(x))


