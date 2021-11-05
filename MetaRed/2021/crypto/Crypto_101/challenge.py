from Crypto.Util.number import *
from binascii import hexlify
import gmpy
from flag import FLAG

flag = FLAG
data = b'potatoespotatoespotatoes'
BITS = 512

flag = int(flag.hex(), 16)
data = int(data.hex(), 16)

p = getStrongPrime(BITS)
q = getStrongPrime(BITS)
r = getStrongPrime(BITS)

n1 = p * q
n2 = q * r

e = 65537

c1 = pow(flag, e, n1)
c2 = pow(data, e, n2)

print("n1=" + str(n1))
print("n2=" + str(n2))
print("e=" + str(e))
print("c1=" + str(c1))
print("c2=" + str(c2))
