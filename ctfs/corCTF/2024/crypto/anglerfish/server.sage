#!/usr/bin/sage

import sys
print("I caught an anglerfish in the sea! ")
sys.stdout.flush()

from hashlib import sha256
from Crypto.Util.number import bytes_to_long
from random import SystemRandom
import ast

n = 100
m = 100
q = 5
FF.<x> = GF(q)

def apply(F, v):
    out = []
    for i in range(m):
        out.append((v.T * F[i] * v)[0, 0])
    return matrix(FF, m, 1, out)

def apply_verif_info(F, a, b):
    out = []
    for i in range(m):
        out.append((a.T * (F[i] + F[i].T) * b)[0, 0])
    return matrix(FF, m, 1, out)

def create_pok(v, s, F):
    proofs = []
    for i in range(64):
        t = matrix(FF, n, 1, [FF.random_element() for i in range(n)])
        com = apply(F, t)
        verif = apply_verif_info(F, t, s)
        a = list(FF)[sha256(bytes([list(FF).index(i[0]) for i in list(com) + list(v) + list(verif)])).digest()[0] % len(list(FF))]
        proofs.append((com, t - a * s, verif))
    return proofs

def verif_pok(v, F, pis):
    coms = []
    for pi in pis:
        com = pi[0]
        assert com not in coms
        coms.append(com)
        resp = pi[1]
        verif = pi[2]
        a = list(FF)[sha256(bytes([list(FF).index(i[0]) for i in list(com) + list(v) + list(verif)])).digest()[0] % len(list(FF))]
        out1 = apply(F, resp)
        out2 = com + (a * a) * v - a * verif
        assert out1 == out2

rng = SystemRandom()
gen_seed = []

for i in range(64):
    gen_seed.append(rng.randint(0, 255))

init_seed = gen_seed
gen_seed = bytes(gen_seed)

F = []

for i in range(m):
    cur = []
    for j in range(n):
        cur.append([])
        for k in range(n):
            cur[-1].append(list(FF)[sha256(gen_seed).digest()[0] % len(list(FF))])
            gen_seed = sha256(gen_seed).digest()
    F.append(matrix(FF, n, n, cur))

s = random_matrix(FF, n, 1)

v = apply(F, s)

pok = create_pok(v, s, F)
verif_pok(v, F, pok)

for pi in pok:
    print("m0 =", [list(FF).index(i[0]) for i in list(pi[0])])
    print("m1 =", [list(FF).index(i[0]) for i in list(pi[1])])
    print("m2 =", [list(FF).index(i[0]) for i in list(pi[2])])

print("Can you catch an anglerfish? ")
print("seed =", [int(i) for i in init_seed])
print("v =", [list(FF).index(i[0]) for i in v])

pis = []
for x in range(64):
    m0 = [int(i) for i in ast.literal_eval(input("m0 = "))]
    m1 = [int(i) for i in ast.literal_eval(input("m1 = "))]
    m2 = [int(i) for i in ast.literal_eval(input("m2 = "))]

    for pi in pok:
        assert(m0 != [list(FF).index(i[0]) for i in list(pi[0])])
        assert(m1 != [list(FF).index(i[0]) for i in list(pi[1])])
        assert(m2 != [list(FF).index(i[0]) for i in list(pi[2])])

    m0 = matrix(FF, m, 1, [list(FF)[i] for i in m0])
    m1 = matrix(FF, n, 1, [list(FF)[i] for i in m1])
    m2 = matrix(FF, m, 1, [list(FF)[i] for i in m2])

    assert m0 not in [pi[0] for pi in pok]
    assert m1 not in [pi[1] for pi in pok]
    assert m2 not in [pi[2] for pi in pok]

    pi = (m0, m1, m2)
    pis.append(pi)

verif_pok(v, F, pis)

with open("flag.txt", "r") as f:
    print(f.read())
