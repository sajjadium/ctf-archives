from Crypto.Util.number import getPrime, bytes_to_long
from random import randint, choices
from string import ascii_uppercase, digits
import signal

with open('flag.txt', 'rb') as f:
    flag = f.read()

signal.alarm(300)

q = getPrime(160)
while True:
    key = "rctf_" + "".join(choices(ascii_uppercase + digits, k=15))
    x = bytes_to_long("".join(sorted(key)).encode())
    if x < q:
        break
l = 2
T = []
U = []
for i in range(90):
    t = randint(1, q)
    u = x * t - randint(1, q >> l)
    T.append(t)
    U.append(u)

print(f"q = {q}")
print(f"T = {T}")
print(f"U = {U}")

guess = int(input("x = ").strip())
if guess == x:
    print(flag)