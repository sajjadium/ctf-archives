from itertools import *
from gmpy2 import *
def x(a,b):
    return bytes(islice((x^y for x,y in zip(cycle(a), cycle(b))), max(*map(len, [a, b]))))
def t(x):
    return sum((((x & 28) >> 4) & 1) << i for i, x in enumerate(x))
T = t(x(b"jctf{not_the_flag}", b"*-*")) | 1
with open("flag.txt", "rb") as f:
    flag = int.from_bytes(f.read(), "little")
    l = flag.bit_length()
print(f"{l = }")
for _ in range(421337):
    flag = (flag >> 1) | ((popcount(flag & T) & 1) << (l - 1))
print(f"{flag = }")

### Output
# l = 420
# flag = 2535320453775772016257932121117911974157173123778528757795027065121941155726429313911545470529920091870489045401698656195217643
###
