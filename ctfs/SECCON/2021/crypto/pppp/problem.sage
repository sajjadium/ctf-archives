from Crypto.Util.number import *
from flag import flag

p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q

mid = len(flag) // 2

e = 65537

m1 = int.from_bytes(flag[:mid], byteorder='big')
m2 = int.from_bytes(flag[mid:], byteorder='big')

assert m1 < 2**256
assert m2 < 2**256

m = [[p,p,p,p], [0,m1,m1,m1], [0,0,m2,m2],[0,0,0,1]]

# add padding
for i in range(4):
    for j in range(4):
        m[i][j] *= getPrime(768)

m = matrix(Zmod(p*q), m)

c = m^e

print("n =", n)
print("e =", e)
print("c =", list(c))