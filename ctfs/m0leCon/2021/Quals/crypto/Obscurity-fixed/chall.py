import random
from functools import reduce
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

pt = "Look, a new flag: " + flag
pt = pt.encode()

lfsr_len = [random.randint(4,6) for _ in range(random.randint(9,12))]
L = [buildLFSR(i) for i in lfsr_len]
u = 0
key = b""
for i in range(len(pt)):
    ch = 0
    for j in range(8):
        outvec = [l.clock() for l in L]
        out = (reduce(lambda i, j: i^j, outvec) ^ u) & 1
        u = (u+sum(outvec))//2
        ch += out*pow(2,7-j)
    key += bytes([ch])

res = xor(key,pt).hex()
print(res)
