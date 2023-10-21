#!/usr/bin/sage
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import md5
import signal
import random
import os
FLAG = os.environ.get('FLAG', 'n1ctf{XXXXFAKE_FLAGXXXX}')

class ECPrng:
    def __init__(self):
        self.N = self.keygen()
        self.E = EllipticCurve(Zmod(self.N), [3, 7])
        self.bias = random.randint(1, 2^128)
        self.state = None
        print(f"N = {self.N}")
        
    def keygen(self):
        P = getPrime(256)
        while True:
            q = getPrime(256)
            if is_prime(2*q-1):
                Q = 2*q^2-q
                return P*Q
    
    def setState(self, x0, y0):
        self.state = self.E(x0, y0)
    
    def next(self):
        self.state = 4*self.state
        return int(self.state.xy()[0])+self.bias

def v2l(v):
    tp = []
    for item in v:
        tp.append(item.list())
    return tp

def Sample(eta, num, signal=0):
    if signal:
        random.seed(prng.next())
    s = []
    for _ in range(num):
        if random.random() < eta:
            s.append(1)
        else:
            s.append(0)
    return Rq(s)

class P:
    def __init__(self, A, s, t):
        self.A = A
        self.s = s
        self.t = t
        self.y = None
    
    def generateCommit(self, Verifier):
        self.y = vector(Rq, [Sample(0.3, N, 1) for _ in range(m)])
        w = self.A * self.y
        Verifier.w = w
        print(f"w = {w.list()}")
        
    def generateProof(self, Verifier, c):
        z = self.s*c + self.y
        print(f"z = {v2l(z)}")
        Verifier.verifyProof(z)

class V:
    def __init__(self, A, t):
        self.A = A
        self.t = t
        self.w = None
        self.c = None
        
    def challenge(self, Prover):
        self.c = Sample(0.3, N)
        print(f"c = {self.c.list()}")
        Prover.generateProof(self, self.c)
        
    def verifyProof(self, z):
        if self.A*z == self.t*self.c + self.w:
            return True
        return False

def Protocol(A, secret, t):
    prover = P(A, secret, t)
    verifier = V(A, t)
    prover.generateCommit(verifier)
    verifier.challenge(prover)

if __name__ == "__main__":
    try:
        signal.alarm(120)
        print("ECPRNG init ...")
        prng = ECPrng()
        x0, y0 = input("PLZ SET PRNG SEED > ").split(',')
        prng.setState(int(x0), int(y0))
        N, q, m = (256, 4197821, 15)
        PRq.<a> = PolynomialRing(Zmod(q))
        Rq = PRq.quotient(a^N + 1, 'x')
        A = vector(Rq, [Rq.random_element() for _ in range(m)])
        secret = vector(Rq, [Sample(0.3, N) for _ in range(m)])
        t = A*secret
        print(f"A = {v2l(A)}")
        print(f"t = {t.list()}")
        Protocol(A, secret, t)
        cipher = AES.new(md5(str(secret).encode()).digest(), mode=AES.MODE_ECB)
        print(f"ct = {cipher.encrypt(pad(FLAG.encode(), 16)).hex()}")
    except:
        print("error!")