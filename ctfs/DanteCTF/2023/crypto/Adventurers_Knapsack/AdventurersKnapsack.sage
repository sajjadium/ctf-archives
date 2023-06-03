from SECRET import flag, privk, m, n
from sage.numerical.knapsack import Superincreasing

flag_int=bytes_to_long(flag)
L=len(flag)*8
assert L==176

assert Superincreasing(privk).is_superincreasing()
assert m > sum(privk)
assert gcd(n,m) == 1

pubk= [(n*i)%m for i in privk]
shuffle(pubk)

ct=0
for i in range(L):
    if flag_int & 2^(L-i-1) != 0:
        ct += pubk[i]

print(f'{ct=}')
print(f'{pubk=}')


