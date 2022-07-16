from secret import p, q
from sage.all import factor

for r in [p, q]:
    for s, _ in factor(r - 1):
        assert int(s).bit_length() <= 25

n = p * q
e = 0x10001

with open("flag.txt", "rb") as f:
    flag = int.from_bytes(f.read().strip(), "big")
assert flag < n

ct = pow(flag, e, n)
print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")
