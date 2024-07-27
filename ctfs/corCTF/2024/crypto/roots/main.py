from Crypto.Util.number import getPrime, bytes_to_long
from random import getrandbits
from decimal import Decimal, getcontext
from secret import FLAG

N = 3
MSIZE = 64
PSIZE = 128

getcontext().prec = 2024

def chunk(inp: bytes, n: int) -> list[bytes]:
    return [inp[i:i + n] for i in range(0, len(inp), n)]

def generate() -> list[int]:
    return sorted(getPrime(PSIZE) for _ in range(N))

def otp(data: int) -> list[int]:
    key = [getrandbits(MSIZE) for _ in range(N - 1)]

    # Apply multiple times for extra security! ;)
    for k in key:
        data ^= k

    return key + [data]

def enc(data: int, key: list[int]) -> Decimal:
    return sum(a * Decimal(p).sqrt() for a, p in zip(otp(data), key))

def encrypt(plaintext: bytes, key: list[int]) -> Decimal:
    out = []
    for pt in chunk(plaintext, MSIZE // 8):
        out.append(enc(bytes_to_long(pt), key))

    return out

def main() -> None:
    key = generate()
    ct = encrypt(FLAG, key)

    print(ct)

if __name__ == "__main__":
    main()
