from Crypto.Util.number import getPrime
from random import randint
from math import gcd
from functools import reduce
from hashlib import sha256

from typing import List, Tuple


def product(l: List[int]) -> int:
    return reduce(lambda a, b: a*b, l)


def gen_params() -> Tuple[int, Tuple[List[int], List[int]]]:

    while True:

        primes = [getPrime(256) for _ in range(16)]
        power = [randint(1, 10) for _ in primes]

        n = product(p**w for p, w in zip(primes, power))

        g = randint(0, n-1)
        if gcd(g, n) != 1:
            continue

        if any(pow(g, p-1, p**w) == 1 for p, w in zip(primes, power)):
            continue

        g = pow(g, product(p-1 for p in primes), n)
        return g, (primes, power)


g, (primes, power) = gen_params()
n = product(p**w for p, w in zip(primes, power))
m = randint(0, product(p**(w-1) for p, w in zip(primes, power)) - 1)
gm = pow(g, m, n)

open("params.py", "w").write("\n".join([
    f"g = {g}",
    f"gm = {gm}",
    f"n = {(primes, power)}"
]))
print("SEE{%s}" % sha256(m.to_bytes((m.bit_length()+7)//8, "little")).hexdigest())
