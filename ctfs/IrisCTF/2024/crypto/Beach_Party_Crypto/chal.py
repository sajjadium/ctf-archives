#!/usr/bin/env pypy3
import secrets
import signal
import hashlib

def tropical_pow(x, y, op):
    if 1 == y:
        return x
    exp = bin(y)
    value = x
 
    for i in range(3, len(exp)):
        value = op(value, value)
        if(exp[i:i+1]=='1'):
            value = op(value, x)
    return value

def pair_add(*a):
    return (max(c[0] for c in a), max(c[1] for c in a))

pair_add_semi = lambda a,b,c: pair_add(a, b)

def pair_mul(a, b):
    return (max(a[0] + b[0], a[1] + b[1]), max(a[0] + b[1], a[1] + b[0]))

def pair_mul_semi(a, b, c):
    return (max(c + a[0] + b[0], c + a[1] + b[1]), max(c + a[0] + b[1], c + a[1] + b[0]))

def semi_factory(c):
    def pair_mul_mat(a, b):
        zb = list(zip(*b))
        return [[pair_add(*[pair_mul_semi(x, y, c) for x, y in zip(row, col)]) for col in zb] for row in a]
    return pair_mul_mat
def pair_mul_mat(a, b):
    zb = list(zip(*b))
    return [[pair_add(*[pair_mul(x, y) for x, y in zip(row, col)]) for col in zb] for row in a]

DIMENSION = 30
LB = -(10**6)
UB =  (10**6)
p = secrets.randbelow(-LB + UB) + LB
q = secrets.randbelow(-LB + UB) + LB
c = secrets.randbelow(-LB + UB) + LB
d = secrets.randbelow(-LB + UB) + LB
k = secrets.randbits(128)
l = secrets.randbits(128)
r = secrets.randbits(128)
s = secrets.randbits(128)

X = []
Y = []
for i in range(DIMENSION):
    X_ = []
    Y_ = []
    for j in range(DIMENSION):
        X_.append((secrets.randbelow(-LB + UB) + LB, secrets.randbelow(-LB + UB) + LB))
        Y_.append((secrets.randbelow(-LB + UB) + LB, secrets.randbelow(-LB + UB) + LB))
    X.append(X_)
    Y.append(Y_)

print("A's work...")
A1 = tropical_pow(X, k, op=semi_factory(c))
A2 = tropical_pow(Y, l, op=semi_factory(c))
A = pair_mul_mat(A1, A2)
A_pub = [[(e[0]+p,e[1]+p) for e in c] for c in A]

print("B's work...")
B1 = tropical_pow(X, r, op=semi_factory(d))
B2 = tropical_pow(Y, s, op=semi_factory(d))
B = pair_mul_mat(B1, B2)
B_pub = [[(e[0]+q,e[1]+q) for e in c] for c in B]

print("Computing keys")
K_a = pair_mul_mat([[(e[0]+p,e[1]+p) for e in c] for c in A1], pair_mul_mat(B_pub, A2))
K_b = pair_mul_mat([[(e[0]+q,e[1]+q) for e in c] for c in B1], pair_mul_mat(A_pub, B2))

assert all(a == b for c1, c2 in zip(K_a, K_b) for a, b in zip(c1, c2))

print("X=")
print(X)
print("Y=")
print(Y)
print("A_pub =")
print(A_pub)
print("B_pub =")
print(B_pub)

h = hashlib.sha256(repr(K_a).encode()).hexdigest()

signal.alarm(60)
guess = input("What's my hash? ")

if h == guess:
    with open("flag") as f:
        print(f.read())
else:
    print("Sorry.")
