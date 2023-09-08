from Crypto.Util.number import *
from functools import reduce
from random import SystemRandom
import os

random = SystemRandom()


def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


with open("flag.txt", "rb") as f:
    flag = f.read().strip()

n_size = 1024
msgs = [os.urandom(n_size // 8 - 1) for _ in range(3)]
msgs += [reduce(xor, msgs + [flag])]
msgs = [bytes_to_long(m) for m in msgs]
pubs = [getPrime(n_size // 2) * getPrime(n_size // 2) for _ in range(100)]

cts = []
for pub in pubs:
    random.shuffle(msgs)
    cur = []
    for m in msgs:
        a = getRandomRange(0, pub)
        b = getRandomRange(0, pub)
        c = pow(a * m + b, 11, pub)
        cur.append((a, b, c))
    cts.append(cur)

print(f"{pubs = }")
print(f"{cts = }")
