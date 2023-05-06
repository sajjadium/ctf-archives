from Crypto.Util.number import *
from Crypto.Random.random import *


p = getPrime(1024)
q = getPrime(1024)

n = p*q

flag = bytes_to_long(open("flag.txt", "rb").read())

iv = getrandbits(1024)

def genPoly(iv):
    ret = []
    s = 0
    for i in range(64, 0, -1):
        a = getrandbits(1024)
        ret.append(a)
        s+=a*pow(iv, i, n)
        s%=n
    ret.append(p-(s%p))
    return ret


with open("output.txt", "w") as f:
    f.write(str(n))
    f.write("\n")
    f.write(str(pow(flag, 65537, n)))
    f.write("\n")
    f.write(str(genPoly(iv)))
    f.write("\n")
    f.write(str(genPoly(iv)))
    f.write("\n")
