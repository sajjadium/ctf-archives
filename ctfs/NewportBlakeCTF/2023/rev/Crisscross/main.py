import random

key1 = random.choices(range(256), k=20)
key2 = list(range(256))
random.shuffle(key2)
flag = open('flag.txt', 'rb').read()    

def enc(n):
    q = key2[n]
    w = key1[q % 20]
    n ^= q
    return n, w

x = 0
for i, c in enumerate(flag):
    x <<= 8
    n, w = enc(c)
    if i % 2:
        n, w = w, n
    x |= n
    x |= w << ((2 * i + 1) * 8)

print(key1)
print(key2)
print(x)