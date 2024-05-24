from sage.all import *
from Crypto.Util.number import getPrime, isPrime
import os

def get_random(n):
    return int.from_bytes(os.urandom(n//8  + 1), "big")

def get_safe_prime(nbit):
    result = 2 * getPrime(nbit // 2) * getPrime(nbit // 2) + 1
    while not isPrime(int(result)):
        result = 2 * getPrime(nbit // 2) * getPrime(nbit // 2) + 1
    return result


FLAG = int.from_bytes(open("flag.txt", "rb").read().strip(), "big")

nbit = 1024

p = get_safe_prime(nbit // 2)
q = get_safe_prime(nbit // 2)
n = p*q

Mat = matrix(Zmod(n), [
    [2, 1] + [get_random(nbit) for _ in range(4)],
    [0, 2] + [get_random(nbit) for _ in range(4)],
    [0, 0] + [4, 1] + [get_random(nbit) for _ in range(2)],
    [0, 0] + [0, 4] + [get_random(nbit) for _ in range(2)],
    [0, 0] + [0, 0] + [8, 1],
    [0, 0] + [0, 0] + [0, 8]
])

C = Mat^FLAG
C = list(C)

with open("output.txt", "w") as f:
    f.write(f"{C = }")