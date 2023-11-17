from random import randint
from re import search
from flag import FLAG

cs = [randint(0, 2**1000) for _ in range(10)]
xs = [randint(0, 2**64) for _ in range(10)]
xs = [ord(f) + i - (i%1000)  for i, f in zip(xs, search("{(.*)}", FLAG).group(1))]

print(f"{cs = }")
print(f"s = {sum(c*x for c, x in zip(cs, xs))}")
