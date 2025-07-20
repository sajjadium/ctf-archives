from sage.all import *
import json
from hashlib import sha256
import os
import secrets
import random
from tqdm import tqdm
from multiprocessing import Pool

Q = 8380417
K = 4
L = 4
ETA = 2
TAU = 39
BETA = 78
GAMMA1 = (1 << 17)
GAMMA2 = ((Q-1)/88)
N = 256

F = GF(Q)
P, X = PolynomialRing(F, 'X').objgen()
R, tbar = P.quotient_ring(X**N + 1, 'tbar').objgen()

def sample_small_poly(mu, n):
    return R([secrets.randbelow(2 * mu + 1) - mu for _ in range(n)])

def keygen():
    seed = os.urandom(32)
    set_random_seed(int.from_bytes(seed, "big"))
    A = random_matrix(R, K, L)
    s1 = vector(R, [sample_small_poly(ETA, N) for _ in range(L)])
    s2 = vector(R, [sample_small_poly(ETA, N) for _ in range(K)])
    t = A * s1 + s2
    return (seed, t), (A, s1, s2)

def center_s(s, p):
    t = int(s) % p
    return t - p if t > p // 2 else t

def center_vec(v, p):
    return [[center_s(s, p) for s in pol] for pol in v]

def high_bits(vf):
    vz = [[int(s) for s in pol] for pol in vf]
    vlo = center_vec(vz, 2 * GAMMA2)
    vhi = [[(x-y) // (2 * GAMMA2) for x, y in zip(pol, pol2)] for pol, pol2 in zip(vz, vlo)]
    return vector(R, vhi)

def hash_2_ball(msg, w1, N):
    pre = msg.encode() + b'\xff' + str(w1).encode()
    h = sha256(pre).digest()

    # Not exactly ideal, but no intended vulnerability here
    r = random.Random(h)
    inds = r.sample(range(N), TAU)
    signs = [1 - 2*r.randint(0, 1) for _ in range(TAU)]
    c = [0 for _ in range(N)]
    for i in range(TAU):
        c[inds[i]] = signs[i]
    return R(c)

def sign_d(msg):
    while 1:
        y = vector(R, [sample_small_poly(ETA, N) for _ in range(L)])
        w = A * y
        w1 = high_bits(w)
        c = hash_2_ball(msg, w1, N)
        z = y + c * s1
        zc = center_vec(z, Q)
        if all(abs(x) < GAMMA1 - BETA for pol in zc for x in pol):
            zl = [[int(x) for x in pol] for pol in z]
            cl = [int(center_s(cc, Q)) for cc in c]
            return (zl, cl, msg)
    else:
        import sys
        sys.exit(1)

# This is just for speed, otherwise signature generation would take ages
def sign_bulk(msgs):
    sigs = {}
    for msg in msgs:
        zl, cl, m = sign_d(msg)
        sigs[m] = [zl, cl]
    return sigs

NSIGS = 1<<19
NTH = os.cpu_count() + 1

pk, sk = keygen()
seed, t = pk
A, s1, s2 = sk

rnd_string = os.urandom(16 * NSIGS).hex()
msgs = [
    rnd_string[i:i+32] for i in range(0, len(rnd_string), 32)
]

STEP = 1<<8
chks = [msgs[i:i+STEP] for i in range(0, NSIGS, STEP)]

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
flag = open("flag.txt", "rb").read()
k = sha256(str([s1, s2]).encode()).digest()
enc = AES.new(k, AES.MODE_ECB).encrypt(pad(flag, 16))

f = open("output.txt", "w")
f.write(json.dumps({
    'seed': seed.hex(),
    't': [[int(x) for x in pol] for pol in t],
    'ct': enc.hex(),
}) + "\n")

# Also for speed.
with Pool(NTH) as pool:
    for out in tqdm(pool.imap(sign_bulk, chks), total=len(chks)):
        for msg, (zl, cl) in out.items():
            f.write(json.dumps([msg, zl, cl]) + "\n")
