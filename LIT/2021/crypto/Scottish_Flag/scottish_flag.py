import random
import binascii
import math
import sympy


def d(x0,x1,y0,y1):
    return (x0-y0)**2 + (x1-y1)**2

class PRNG:
    def __init__(self,seed0,seed1):
        self.seed0 = seed0;
        self.seed1 = seed1;
        self.L = 1;

    # Returns a random number between [0,x)
    def rand(self,x0,x1):
        return d(self.seed0, self.seed1, x0, x1)


def str2Dec(str):
    return int(binascii.hexlify(str.encode("utf-8")),16);

flag = open('flag.txt','rb').read().decode("utf-8");
flag0 = flag[:len(flag) // 2];
flag1 = flag[len(flag) // 2:len(flag)];

ct0 = str2Dec(flag0);
ct1 = str2Dec(flag1);

g = PRNG(ct0,ct1);
a0 = 1000000000000000000;
a1 = random.randint(0,1000000000000000000);

print(g.rand(0,a0));
print(g.rand(a1,0));
print(g.rand(a1,a0));