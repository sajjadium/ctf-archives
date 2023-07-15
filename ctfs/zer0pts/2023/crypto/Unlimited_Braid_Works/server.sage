import sys
import random
import string
import hashlib
from Crypto.Util.number import *

flag = os.environb.get(b"FLAG", b"dummmmy{test_test_test}")

def hash(b):
	return hashlib.sha512(str(b).encode("utf-8")).digest()

n = int(input("Input the security parameter> "))
if n < 16:
	print("The security parameter is too small !!")
	sys.exit(1)

if (n & 1) == 1:
	print("The security parameter must be even !!")
	sys.exit(1)

print(f"n: {n}")

## ------------------
## Key Generation
## ------------------

Bn = BraidGroup(n)
gs = Bn.gens()

K = 32
u = random.choices(gs, k=K)

# u must be twisted
if not gs[n // 2 - 1] in u:
	u[randint(0, K - 1)] = gs[n // 2 - 1]

u = prod(u)
print(f"u: {prod(u.right_normal_form())}")

al = prod(random.choices(gs[: n//2-2], k=K))
v = al * u * al^-1

print(f"v: {prod(v.right_normal_form())}")

## ------------------
## Encryption
## ------------------

pad_length = 64 - len(flag)
left_length = random.randint(0, pad_length)
pad1 = "".join(random.choices(string.ascii_letters, k=left_length)).encode("utf-8")
pad2 = "".join(random.choices(string.ascii_letters, k=pad_length-left_length)).encode("utf-8")
flag = pad1 + flag + pad2

br = prod(random.choices(gs[n//2 + 1 :], k=K))
w = br * u * br^-1
c = br * v * br^-1
h = hash(prod(c.right_normal_form()))

d = []
for i in range(len(h)):
	d.append(chr(flag[i] ^^ h[i]))
d = bytes_to_long("".join(d).encode("utf-8"))

print(f"w: {prod(w.right_normal_form())}")
print(f"d: {d}")
