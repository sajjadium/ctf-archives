#!/bin/python3

import hashlib
from math import gcd
import random

def generate_inv_elem(n):
  while True:
    k = random.randint(1, n)
    if gcd(k, n) == 1:
        return k

with open("flag", "rb") as f:
  flag = f.read()

assert len(flag) == 32
flag = random.randbytes(128 - 32) + flag

x = int.from_bytes(flag, 'big')
p = pow(2, 1024) + 643

with open("to-sign", "r") as f:
  m = f.read()

assert len(m) % 2 == 0
SIZE = len(m) // 2

signature = b""
k = generate_inv_elem(p - 1)
for i in range(0, len(m), SIZE):
  g = generate_inv_elem(p)
  r = pow(g, k, p)
  h_m = int.from_bytes(hashlib.sha256(m[i: i+SIZE].encode()).digest(), 'big') % (p - 1)
  s = ((h_m - x * r) * pow(k, -1, p - 1)) % (p - 1)
  signature += g.to_bytes(256, 'big') + r.to_bytes(256, 'big') + s.to_bytes(256, 'big')

with open("signature", "wb") as f:
  m = f.write(signature)

