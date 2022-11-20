#!/usr/bin/env python3
import random

with open('flag.txt', 'r') as f:
    flag = f.read()

seed = random.randint(0,999)
random.seed(seed)

encrypted = ''.join(f'{(ord(c) ^ random.randint(0,255)):02x}' for c in flag)

with open('out.txt', 'w') as f:
    f.write(encrypted)
