#!sage
import random
from hashlib import sha256
from Crypto.Util.number import *

class KeyPredistribution:
    # a key predistribution scheme in 《A Random Perturbation-Based Scheme for Pairwise Key Establishment in Sensor Networks》
    def __init__(self ,p , t ,r , N):
        self.p = p
        self.t = t
        self.r = r
        self.N = N
        self.F = self.random_symmetric_polynomial()
        self.random_perturbation_polynomials()
    def random_symmetric_polynomial(self):
        P = PolynomialRing(GF(self.p) , "x,y")
        x , y = P.gens()
        F = 0
        for i in range(self.t+1):
            for j in range(self.t+1):
                r = GF(self.p).random_element()
                F += r * x^i * y^j +r * y^i * x^j 
        return F
    def random_perturbation_polynomials(self):
        P = PolynomialRing(GF(self.p) , 'y')
        g = P.random_element(degree = self.t , total = self.t+1)
        h = P.random_element(degree = self.t , total = self.t+1)
        S = []
        while len(S) < self.N:
            e = GF(self.p).random_element()
            if e not in S:
                if g(e) < self.r and h(e) < self.r:
                    S.append(e)
                
        self.g = g
        self.h = h
        self.S = S
    def get_node(self, index):
        if index > len(self.S):
            print("index out of range")
            return 0
        xi = self.S[index]
        _ , y = self.F.parent().gens()
        f = self.F(xi , y)
        r = random.randint(0 , 1)
        f += r*self.g + (1-r)*self.h
        pubkey = xi
        prikey = f
        return (pubkey , prikey)

def share_secret(a_prikey , b_pubkey , r):
    f = a_prikey
    xj = b_pubkey
    share = f(xj) >> (int(log(r , 2))+1)
    return share, sha256(share)
p = 2**48 - 59
r = 2**38
t = 40
n = 43
KP = KeyPredistribution(p , t ,r , n)
hint = KP.F(0,0)
# hint = 35327434352315
f = open('./data.txt' , 'w')
for i in range(n):
    node = KP.get_node(i)
    f.write(str(node) + '\n')
f.close()
flag = 'd3ctf{' + sha256(b''.join([long_to_bytes(int(i)) for i in KP.F.coefficients()])).hexdigest() + '}'
print(flag)