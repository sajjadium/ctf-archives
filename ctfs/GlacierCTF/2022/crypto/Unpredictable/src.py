from Crypto.Util.number import bytes_to_long
from secret import flag, roll_faster, a, b, m
import random

texts = open("txt.txt", "rb").readlines()

def roll(x, y):
    for _ in range(y):
        x = (a*x + b) % m
    return x

print("Im not evil, have some paramteres")
print(f"{a = }")
print(f"{b = }")
print(f"{m = }")

seeds = []
cts = []

for pt in texts:
    x = random.getrandbits(512)
    y = random.getrandbits(512)
    # r = roll(x,y) # This is taking too long
    r = roll_faster(x,y)
    seeds.append(max(x,y))
    cts.append(r ^ bytes_to_long(pt))

print(f"{seeds = }")
print(f"{cts = }")

flag_ct = bytes_to_long(flag) ^ roll_faster(random.getrandbits(512), random.getrandbits(512))

print(f"{flag_ct = }")