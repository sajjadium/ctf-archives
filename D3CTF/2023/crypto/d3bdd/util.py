from Crypto.Util.number import *

class PRNG:
    def __init__(self , seed):
        self.state = bytes_to_seedlist(seed)
        
        self.m = 738136690439
        # f = [randint(0 , m) for _ in range(16)]
        self.f = [172726532595, 626644115741, 639699034095, 505315824361, 372926623247, 517574605128, 185188664643, 151765551359, 246806484646, 313551698318, 366113530275, 546914911952, 246941706000, 157807969353, 36763045564, 110917873937]
        self.mbit = 40
        self.d = 16
        for i in range(self.d):
            self.generate()
    def generate(self):
        res = 0
        for i in range(self.d):
            res += self.f[i] * self.state[i]
            res %= self.m
        self.state = self.state[1:] + [res]
    def raw_rand(self):
        temp = self.state[0]
        self.generate()
        return temp



q = 2**32-5
n = 512
class polynomial:
    
    # polynomial in Zq[x]/(x^n - 1)

    def __init__(self,flist):
        if type(flist) == list:
            assert len(flist) == n
            self.f = [flist[i] % q for i in range(n)]

    def __add__(self , other):
        assert type(other) == polynomial
        return polynomial([(self.f[i] + other.f[i])%q for i in range(n)])
    def __sub__(self , other):
        assert type(other) == polynomial
        return polynomial([(self.f[i] - other.f[i])%q for i in range(n)])
    def __mul__(self , other):
        assert type(other) == polynomial
        res = [0]*n
        for i in range(n):
            for j in range(n):
                res[(i+j)%n] += self.f[i] * other.f[j]
                res[(i+j)%n] %= q
        return polynomial(res)

def bytes_to_seedlist(seedbytes):
    seedlist = []
    for i in range(16):
        seedlist.append(bytes_to_long(seedbytes[i*4:i*4+4]))
    return seedlist

def sample_poly(seed , lower , upper):
    prng = PRNG(seed)
    polylist = []
    for i in range(n):
        polylist.append((prng.raw_rand() % (upper - lower)) + lower)
    return polynomial(polylist)
def encode_m(m):
    m = bytes_to_long(m)
    flist = []
    for i in range(n):
        flist = [m&1] + flist
        m >>= 1
    return polynomial(flist)
