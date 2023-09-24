FLAG = open('flag.txt', 'rb').read()
import random
import hashlib
MOD = 20000159
N = MOD
K = N - 3
poly = [random.randrange(MOD) for i in range(K)]
print([x^y for x,y in zip(hashlib.sha512(str(poly).encode()).digest(), FLAG)])
def eval_at(poly, x):
    t = 1
    ret = 0
    for k in poly:
        ret += t * k
        t *= x
        t %= MOD
    return ret % MOD
shares = [-1] * N
for i in range(N):
    if i not in [69, 420, 1337]:
        shares[i] = eval_at(poly, i)
print(shares)
