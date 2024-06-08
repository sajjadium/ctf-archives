from random import getrandbits
from Crypto.Util.number import getPrime
from SECRET import FLAG

BITS = 128
m = getPrime(BITS)
s = getrandbits(BITS - 1)
a = getrandbits(BITS - 1)
b = getrandbits(BITS - 1)

def lcg(s, c):
    return c*(a*s + b) % m

if __name__ == "__main__":
    c = []
    r = s
    for i in FLAG:
        r = lcg(r, ord(i))
        c.append(r)
    print("m = {}\nc = {}".format(m, c))
