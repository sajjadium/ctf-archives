from Crypto.Util.number import getPrime, inverse
from random import randint
from secret import flag

p = getPrime(256)
print(f"p = {p}")
k = list()
flag = flag.hex().encode()
for i in range(len(flag) - 20):
    g = []
    h = []
    for j in range(0, len(flag), 2):
        a, b = flag[j], flag[j + 1]
        m, n = randint(0, p - 1), randint(0, p - 1)
        c, d = m * a, n * b
        e, f = pow(inverse(c, p) + inverse(d, p), 2, p), (m ** 2 * inverse(c, p) * n ** 2 * inverse(d, p)) % p
        g += [m, n]
        h.append(e * inverse(f, p) % p)
    g.append(sum(h) % p)
    k.append(g)

print(f"k = {k}")