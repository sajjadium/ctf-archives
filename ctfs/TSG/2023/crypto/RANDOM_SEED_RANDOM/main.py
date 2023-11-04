import os
import random
import string

flag = os.getenv("FLAG", "FAKECTF{THIS_IS_FAKE}")

key = [random.randrange(10 ** 4) for _ in flag]
cs = string.printable[:-6]

def r(k):
    for _ in range(k):
        random.seed(x := random.randrange(20231104, 20231104 * 10))
    return x

random.seed(int(input("seed: ")))
print('flag:', ''.join([cs[(cs.index(f) + r(k)) % len(cs)] for f, k in zip(flag, key)]))
