import os
from Crypto.Util.number import getPrime, getRandomRange

with open("flag.txt", "rb") as f:
    m = f.read().strip()
    m += os.urandom(111 - len(m))
    m = int.from_bytes(m, "big")

xs = []
for i in range(11):
    p = getPrime(512)
    q = getPrime(512)
    n = p  * q

    c = m**11 * getRandomRange(0, 2**11) % n

    xs.append((c, n))

print(xs)
