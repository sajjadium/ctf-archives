#!/usr/bin/env sage
import struct
from random import SystemRandom

p = 10000000000000001119

R.<x> = GF(p)[]; y=x
f = y + prod(map(eval, 'yyyyyyy'))
C = HyperellipticCurve(f, 0)
J = C.jacobian()

class RNG(object):

    def __init__(self):
        self.es = [SystemRandom().randrange(p**3) for _ in range(3)]
        self.Ds = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]
        self.q = []

    def clk(self):
        self.Ds = [e*D for e,D in zip(self.es, self.Ds)]
        return self.Ds

    def __call__(self):
        if not self.q:
            u,v = sum(self.clk())
            rs = [u[i] for i in range(3)] + [v[i] for i in range(3)]
            assert 0 not in rs and 1 not in rs
            self.q = struct.pack('<'+'Q'*len(rs), *rs)
        r, self.q = self.q[0], self.q[1:]
        return r

    def __iter__(self): return self
    def __next__(self): return self()

flag = open('flag.txt').read().strip()
import re; assert re.match(r'hxp\{\w+\}', flag, re.ASCII)

text = f"Hello! The flag is: {flag}"
print(bytes(k^^m for k,m in zip(RNG(), text.encode())).hex())

