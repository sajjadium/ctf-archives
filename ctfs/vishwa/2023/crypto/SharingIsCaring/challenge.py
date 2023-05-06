from sympy import randprime
from random import randrange


def generate_shares(secret, k, n):
    prime = randprime(secret, 2*secret)
    coeffs = [secret] + [randrange(1, prime) for _ in range(k-1)]
    shares = []
    for i in range(1, n+1):
        x = i
        y = sum(c * x**j for j, c in enumerate(coeffs)) % prime
        shares.append((x, y))
    return shares, prime


k = 3
n = 5
flag = open('flag.txt', 'rb').read().strip()

for i in flag:
    shares, prime = generate_shares(i, k, n)
    print(shares,prime,sep=', ')




