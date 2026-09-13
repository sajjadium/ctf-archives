#!/usr/bin/env python3

from secrets import FLAG, MOD, B, P, Q

from Crypto.Util.number import bytes_to_long
from leak import known, new

def polynomial_eval(poly, value):
    res = 0
    for i, coeff in enumerate(poly):
        res += coeff * (value**i)
    return res % MOD

def centered(x):
    x %= MOD
    return x if x <= MOD // 2 else x - MOD

# leaked scheme requires 16 shares
# upgraded scheme requires 32
assert len(P) == 16
assert len(Q) == 32
assert len(known) == 16
assert len(new) == 8

# leaked shamir secret shares are still valid
# for backwards compatibility
for x, px in known:
    assert polynomial_eval(P, x) == px
    assert polynomial_eval(Q, x) == px

# freshly issued shares valid for new polynomial
for x, qx in new:
    assert polynomial_eval(Q, x) == qx

# new secret
assert polynomial_eval(Q, 0) == bytes_to_long(FLAG.encode())

for pc, qc in zip(P + [0] * 16, Q):
    assert abs(centered(qc - pc)) < B

## output.txt
print(f"{MOD = }")
print(f"{B = }\n")
print(f"{known = }\n")
print(f"{new = }")
