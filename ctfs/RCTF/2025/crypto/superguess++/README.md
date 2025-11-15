Three years since you faced RCTF 2022 — solved it, or failed to. Let’s see if you’ve truly learned anything about lattice.

from Crypto.Util.number import getPrime
from secrets import randbelow
import signal

with open("flag.txt", "rb") as f:
    flag = f.read()

signal.alarm(300)

q = getPrime(182)
x = randbelow(q)
l = 2
T = []
U = []
for i in range(93):
    t = randbelow(q)
    u = (x * t - randbelow(q >> l)) % q
    T.append(t)
    U.append(u)

print(f"q = {q}")
print(f"T = {T}")
print(f"U = {U}")

guess = int(input("x = ").strip())
if guess == x:
    print(flag)
