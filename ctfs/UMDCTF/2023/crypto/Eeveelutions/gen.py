from Crypto.Util.number import getPrime, inverse, bytes_to_long
from math import gcd
import re
import string
import random


while True:
    p = getPrime(1024)
    q = getPrime(1024)

    n = p * q
    e = 3
    phi = (p-1)*(q-1)

    if gcd(phi, e) == 1:
        d = inverse(e, phi)
        break


with open('flag.txt', 'r') as f:
    flag = f.read().strip()

pad1 = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))
pad2 = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))

evolutions = ['umbreon', 'sylveon', 'jolteon', 'flareon', 'glaceon', 'leafeon']
e1 = random.choice(evolutions)
while True:
    e2 = random.choice(evolutions)
    if e2 != e1:
        break

flag1 = re.sub("eevee", e1, flag) + pad1
flag2 = re.sub("eevee", e2, flag) + pad2

f1 = bytes_to_long(flag1.encode())
f2 = bytes_to_long(flag2.encode())

ct1 = pow(f1, e, n)
ct2 = pow(f2, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"ct1 = {ct1}")
print(f"ct2 = {ct2}")

