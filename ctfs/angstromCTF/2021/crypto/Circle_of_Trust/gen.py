import random
import secrets
import math
from decimal import Decimal, getcontext
from Crypto.Cipher import AES

BOUND = 2 ** 128
MULT = 10 ** 10

getcontext().prec = 50

def nums(a):
    b = Decimal(random.randint(-a * MULT, a * MULT)) / MULT
    c = (a ** 2 - b ** 2).sqrt()
    if random.randrange(2):
        c *= -1
    return (b, c)


with open("flag", "r") as f:
    flag = f.read().strip().encode("utf8")

diff = len(flag) % 16
if diff:
    flag += b"\x00" * (16 - diff)

keynum = secrets.randbits(128)
ivnum = secrets.randbits(128)

key = int.to_bytes(keynum, 16, "big")
iv = int.to_bytes(ivnum, 16, "big")

x = Decimal(random.randint(1, BOUND * MULT)) / MULT
for _ in range(3):
    (a, b) = nums(x)
    print(f"({keynum + a}, {ivnum + b})")

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
enc = cipher.encrypt(flag)
print(enc.hex())
