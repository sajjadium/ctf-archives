from Crypto.Util.number import *
from FLAG import flag

flag = bytes_to_long(flag)
p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 12721
c = pow(flag, e, n)
print(f"{n = }")
print(f"{c = }")

# hints :)
def hx(x):
    return hex(x)[2:]

d = pow(e, -1, (p-1)*(q-1))
print(hx(d)[-64:])
print(hx(p)[:64])
print(hx(p)[96:161])



