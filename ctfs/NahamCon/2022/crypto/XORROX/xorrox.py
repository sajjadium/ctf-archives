#!/usr/bin/env python3

import random

with open("flag.txt", "rb") as filp:
    flag = filp.read().strip()

key = [random.randint(1, 256) for _ in range(len(flag))]

xorrox = []
enc = []
for i, v in enumerate(key):
    k = 1
    for j in range(i, 0, -1):
        k ^= key[j]
    xorrox.append(k)
    enc.append(flag[i] ^ v)

with open("output.txt", "w") as filp:
    filp.write(f"{xorrox=}\n")
    filp.write(f"{enc=}\n")
