#!/usr/bin/sage
from random import randint
from binascii import unhexlify
from sage.all import *
import sys

F = GF(251, names=("z", ))

m = 44
n = 106

O = random_matrix(F, (n - m), m)
O2 = block_matrix(F, 2, 1, [O, identity_matrix(F, m)])

PM = []

z = zero_matrix(F, m, (n - m))

print_elem = lambda x: print(hex(x)[2:].rjust(2, '0'), end='')

print("Don't spill oil.")

for i in range(m):

    P1 = random_matrix(F, (n - m), (n - m))

    for j in range(0, n - m):
        for k in range(0, j):
            P1[j, k] = 0

    P2 = random_matrix(F, (n - m), m)
    P3 = -O.T * P1 * O - O.T * P2

    for j in range(0, m):
        for k in range(j+1, m):
            P3[j, k] += P3[k, j]
            P3[k, j] = 0

    for i in P1:
        for j in i:
            print_elem(j)

    for i in P2:
        for j in i:
            print_elem(j)

    for i in P3:
        for j in i:
            print_elem(j)

    P = block_matrix([ [P1, P2], [z, P3]])
    PM.append(P)

print()

# Deepwater Horizon, Gulf of Mexico
gm = matrix(F, n, 1, [randint(0, 1) for i in range(n)])

for P in PM:
    print_elem((gm.T * P * gm)[0][0])
print()

# Ixtoc I, Gulf of Mexico
for i in O2.columns():
    gm += F.random_element() * matrix(F, n, 1, list(i))

for i in gm:
    print_elem(i[0])
print()

t = random_matrix(F, m, 1)
for i in t:
    print_elem(i[0])

print()


s = [F(i) for i in unhexlify(input().strip())]

if len(s) != n:
    sys.exit(0)

s = matrix(F, n, 1, s)

for i in range(m):
    if (s.T * PM[i] * s)[0][0] != t[i][0]:
        sys.exit(0)

with open("flag.txt", "r") as f:
    print(f.read().strip())
