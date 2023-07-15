from Crypto.Util.number import *
from flag import flag


def getModPrime(modulus):
    p = getPrime(1024)
    p += (modulus - p) % modulus
    p += 1
    iters = 0
    while not isPrime(p):
        p += modulus
    return p


difficulty = 210

flag = bytes_to_long(flag)

# no cheeses here!
b = getModPrime(difficulty**10)

c = inverse(flag, b)
n = pow(c, difficulty, b)

with open('output.txt', 'w') as f:
    f.write(f"{n} {b}")

