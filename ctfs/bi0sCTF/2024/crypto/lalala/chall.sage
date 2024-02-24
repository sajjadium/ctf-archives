from random import randint
from re import search

flag = "bi0sctf{%s}" % f"{randint(2**39, 2**40):x}"

p = random_prime(2**1024)
unknowns = [randint(0, 2**32) for _ in range(10)]
unknowns = [f + i - (i%1000)  for i, f in zip(unknowns, search("{(.*)}", flag).group(1).encode())]

output = []
for _ in range(100):
    aa = [randint(0, 2**1024) for _ in range(1000)]
    bb = [randint(0, 9) for _ in range(1000)]
    cc = [randint(0, 9) for _ in range(1000)]
    output.append(aa)
    output.append(bb)
    output.append(cc)
    output.append(sum([a + unknowns[b]^2 * unknowns[c]^3 for a, b, c in zip(aa, bb, cc)]) % p)

print(f"{p = }")
print(f"{output = }")
