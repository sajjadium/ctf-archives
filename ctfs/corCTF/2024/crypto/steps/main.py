from Crypto.Util.number import getPrime
from random import randint
from hashlib import sha512
from secret import FLAG

p = getPrime(1024)

Pair = tuple[int, int]

def apply(x: Pair, y: Pair) -> Pair:
    z0 = x[0] * y[1] + x[1] * y[0] - x[0] * y[0]
    z1 = x[0] * y[0] + x[1] * y[1]
    return z0 % p, z1 % p

def calculate(n: int) -> Pair:
    out = 0, 1
    base = 1, 1

    while n > 0:
        if n & 1 == 1: out = apply(out, base)
        n >>= 1
        base = apply(base, base)

    return out

def step(x: Pair, n: int):
    '''Performs n steps to x.'''
    return apply(x, calculate(n))

def xor(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b))

def main() -> None:
    g = tuple(randint(0, p - 1) for _ in range(2))
    a = randint(0, p)
    b = randint(0, p)

    A = step(g, a)
    B = step(g, b)

    print(p)
    print(g)
    print(A)
    print(B)

    shared = step(A, b)
    assert shared == step(B, a)

    pad = sha512(str(shared).encode()).digest()
    print(xor(FLAG, pad))

if __name__ == "__main__":
    main()
