from Crypto.Util.number import getPrime
import random

B = 2^4096
flag = randint(1, B) # recover this value, wrap the answer in Dead{}
m = 4
n = 256
ps = [getPrime(128) for _ in range(n)]
S = [[randint(0, ps[i] - 1) for __ in range(m - 1)] + [int(flag % ps[i])] for i in range(n)]

for Si in S:
    random.shuffle(Si)

print(ps)
print(S)