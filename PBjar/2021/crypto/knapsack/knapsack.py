from Crypto.Util.number import getPrime
from sympy import nextprime
from random import randint

flag = open('./flag.txt', 'rb').read().strip()
flagbits = bin(int.from_bytes(flag, 'big'))[2:]

n, r = len(flagbits), getPrime(8)

w = [randint(1, 69)]
for i in range(1, n):
    w.append(randint(sum(w[:i]) + 1, w[-1] * r))

q = nextprime(r * w[-21])

b = [r * i % q for i in w]
c = sum((0 if i == '0' else 1) * j for i, j in zip(flagbits, b))

f = open('./output.txt', 'w')

print('b: ' + str(b), file = f)
print('c: ' + str(c), file = f)

f.close()
