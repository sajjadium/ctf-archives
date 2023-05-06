from sage.all import *
import random
flag = open('flag.txt','rb').read()
class prng:
    co = [random_prime(2**64-1,False,2**63) for i in range(100)]
    n = int(next_prime(2**64))
    def __init__(self):
        self.s = [random.randint(1,self.n) for i in range(100)]
    def next(self):
        self.s.append(vector(self.s).dot_product(vector(self.co))%self.n)
        return self.s.pop(0)
g = prng()
outs = []
for i in range(200):
    outs.append(g.next())
print(outs)
k = "".join([hex(g.next())[2:].zfill(16) for i in range(ceil(len(flag)/8))])[:len(flag)*2]
print("".join([hex(int(k[2*i:2*i+2],16)^flag[i])[2:].zfill(2) for i in range(len(flag))]))
