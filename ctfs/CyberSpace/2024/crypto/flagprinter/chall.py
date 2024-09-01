from out import enc, R
from math import prod

flag = ''
a = [0]
for i in range(355):
    b = [_+1 for _ in a]
    c = [_+1 for _ in b]
    a += b + c

    if i%5 == 0:
        flag += chr(enc[i//5] ^ prod([a[_] for _ in R[i//5]]))
        print(flag)
