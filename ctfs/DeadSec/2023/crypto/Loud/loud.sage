from Crypto.Util.number import getStrongPrime
import random

B = 2^2048
flag = randint(1, B) # recover this value, wrap the answer in Dead{}
m = 5
n = 30
ps = [getStrongPrime(1024) for _ in range(n)]
S = [[randint(0, ps[i] - 1) for __ in range(m - 1)] + [int(flag % ps[i])] for i in range(n)]

for Si in S:
    random.shuffle(Si)

print(ps)
print(S)