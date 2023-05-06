#!/usr/bin/env python3
#
# Polymero
#

# Imports
from Crypto.Util.number import getPrime, isPrime
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from random import randint
from hashlib import sha256


# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

assert len(FLAG) % 8 == 0


# Helper functions
def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def modular_sqrt(a, p):
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


# TickTock class
class TickTock:
    def __init__(self, x, y, P):
        self.x = x
        self.y = y
        self.P = P
        assert self.is_on_curve()
        
    def __repr__(self):
        return '({}, {}) over {}'.format(self.x, self.y, self.P)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.P == other.P
        
    def is_on_curve(self):
        return (self.x*self.x + self.y*self.y) % self.P == 1
    
    def add(self, other):
        assert self.P == other.P
        x3 = (self.x * other.y + self.y * other.x) % self.P
        y3 = (self.y * other.y - self.x * other.x) % self.P
        return self.__class__(x3, y3, self.P)
    
    def mult(self, k):
        ret = self.__class__(0, 1, self.P)
        base = self.__class__(self.x, self.y, self.P)
        while k:
            if k & 1:
                ret = ret.add(base)
            base = base.add(base)
            k >>= 1
        return ret

def lift_x(x, P, ybit=0):
    y = modular_sqrt((1 - x*x) % P, P)
    if ybit:
        y = (-y) % P
    return TickTock(x, y, P)

def domain_gen(bits):
    while True:
        q = getPrime(bits)
        if isPrime(4*q + 1):
            P = 4*q + 1
            break
    while True:
        i = randint(2, P)
        try:
            G = lift_x(i, P)
            G = G.mult(4)
            break
        except: continue
    return P, G

def key_gen():
    sk = randint(2, P-1)
    pk = G.mult(sk)
    return sk, pk

def key_derivation(point):
    dig1 = sha256(b'x::' + str(point).encode()).digest() 
    dig2 = sha256(b'y::' + str(point).encode()).digest() 
    return sha256(dig1 + dig2 + b'::key_derivation').digest()


# Challenge
flagbits = [FLAG[i:i+len(FLAG)//8] for i in range(0,len(FLAG),len(FLAG)//8)]

for i in range(8):

    print('# Exchange {}:'.format(i+1))

    P, G = domain_gen(48)

    print('\nP =', P)
    print('G = ({}, {})'.format(G.x, G.y))

    alice_sk, alice_pk = key_gen()
    bobby_sk, bobby_pk = key_gen()

    assert alice_pk.mult(bobby_sk) == bobby_pk.mult(alice_sk)

    print('\nA_pk = ({}, {})'.format(alice_pk.x, alice_pk.y))
    print('B_pk = ({}, {})'.format(bobby_pk.x, bobby_pk.y))

    key = key_derivation(alice_pk.mult(bobby_sk))
    cip = AES.new(key=key, mode=AES.MODE_CBC)
    enc = cip.iv + cip.encrypt(pad(flagbits[i], 16))

    print('\nflagbit_{} = "{}"'.format(i+1, enc.hex()))
    print('\n\n\n')

