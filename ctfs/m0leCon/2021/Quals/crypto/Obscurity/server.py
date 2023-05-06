import random
from functools import reduce
import sys
from math import log2
from secret import flag

def xor(a, b):
    return bytes(x^y for x,y in zip(a,b))

class LFSR(object):
    def __init__(self, s, p):
        self.s = s
        self.p = p

    def clock(self):
        out = self.s[0]
        self.s = self.s[1:]+[self.s[0]^self.s[(self.p)[0]]^self.s[(self.p)[1]]]
        return out

def buildLFSR(l):
    return LFSR([int(x) for x in list(bin(random.randint(1,2**l-1))[2:].rjust(l,'0'))], random.sample(range(1,l), k=2))

key = b""

print("encrypt plz [in hex]")
pt = bytes.fromhex(input().strip())

if len(pt)>1000:
    print("WELL, not that much")
    exit()

pt = pt + flag
periodic = True

while periodic:
    lfsr_len = [random.randint(4,6) for _ in range(random.randint(9,12))]
    L = [buildLFSR(i) for i in lfsr_len]
    u = 0
    key = b""
    for i in range(len(pt)+65):
        ch = 0
        for j in range(8):
            outvec = [l.clock() for l in L]
            u = (u+sum(outvec))//2
            out = (reduce(lambda i, j: i^j, outvec) ^ u) & 1
            ch += out*pow(2,7-j)
        key += bytes([ch])
    kk = key.hex()
    if kk.count(kk[-6:]) == 1:
        periodic = False

res = xor(key[:-65],pt).hex()
print(res)
