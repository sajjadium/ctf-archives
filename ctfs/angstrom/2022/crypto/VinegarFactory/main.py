#!/usr/local/bin/python3

import string
import os
import random

with open("flag.txt", "r") as f:
    flag = f.read().strip()

alpha = string.ascii_lowercase

def encrypt(msg, key):
    ret = ""
    i = 0
    for c in msg:
        if c in alpha:
            ret += alpha[(alpha.index(key[i]) + alpha.index(c)) % len(alpha)]
            i = (i + 1) % len(key)
        else:
            ret += c
    return ret

inner = alpha + "_"
noise = inner + "{}"

print("Welcome to the vinegar factory! Solve some crypto, it'll be fun I swear!")

i = 0
while True:
    if i % 50 == 49:
        fleg = flag
    else:
        fleg = "actf{" + "".join(random.choices(inner, k=random.randint(10, 50))) + "}"
    start = "".join(random.choices(noise, k=random.randint(0, 2000)))
    end = "".join(random.choices(noise, k=random.randint(0, 2000)))
    key = "".join(random.choices(alpha, k=4))
    print(f"Challenge {i}: {start}{encrypt(fleg + 'fleg', key)}{end}")
    x = input("> ")
    if x != fleg:
        print("Nope! Better luck next time!")
        break
    i += 1
