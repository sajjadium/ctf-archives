import numpy as np
import secrets

def rand(seed):
    seeds = [(seed >> (3 * i)) & 7 for i in range(nseeds)]
    a = 5
    b = 7
    while True:
        for i in range(nseeds):
            seeds[i] = (a * seeds[i] + b) & 7
            yield seeds[i]

q = 2**142 + 217
n = 69
nseeds = 142
rng = rand(secrets.randbits(3 * nseeds))
with open("flag.txt", "rb") as f:
    flag = f.read().strip()
bits = f'{int.from_bytes(flag, "big"):0{len(flag) * 8}b}'
s = np.array([secrets.randbits(1) for _ in range(n)])

for bit in map(int, bits):
    A = np.array([secrets.randbelow(q) for _ in range(n * n)]).reshape((n, n))
    b = [A @ s + np.array([next(rng) for _ in range(n)]), np.array([secrets.randbelow(q) for _ in range(n)])][bit]
    print(list(map(hex, A.reshape(-1))), list(map(hex, b % q)))
