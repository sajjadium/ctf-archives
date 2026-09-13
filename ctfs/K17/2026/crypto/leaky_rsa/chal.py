#!/usr/bin/env python3

from secrets import FLAG, P, Q

from Crypto.Util.number import bytes_to_long

assert P.bit_length() == 1024
assert Q.bit_length() == 1024
e = 257

# set up parameters
phi = (P - 1) * (Q - 1)

N = P * Q
d = pow(e, -1, phi)

# encrypt
m = bytes_to_long(FLAG)
assert m < N
c = pow(m, e, N)

# crt params for fast decryption
dp = d % (P - 1)
dq = d % (Q - 1)

qinv = pow(Q, -1, P)
dsum = dp + dq

# output
with open("out.txt", "w") as f:
    f.write(f"N = {N}\n")
    f.write(f"e = {e}\n")
    f.write(f"leak = {dsum}\n")
    f.write(f"c = {c}\n")
