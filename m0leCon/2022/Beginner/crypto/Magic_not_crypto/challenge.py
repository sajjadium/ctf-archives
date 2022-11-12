# The following imports are from the pycryptodome library
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
import hashlib
import base64
import random
import os


def RSA(x: bytes) -> bytes:
    e = 65537
    random.seed(bytes_to_long(x[:4]))
    p = getPrime(1024, randfunc=random.randbytes)
    q = getPrime(1024, randfunc=random.randbytes)
    N = p * q
    return long_to_bytes(pow(bytes_to_long(x), e, N))


def rot13(x: bytes) -> bytes:
    return x.translate(bytes.maketrans(
        bytes([i for i in range(256)]),
        bytes([(i + 13) % 256 for i in range(256)])
    ))


possible_methods = [
    base64.b64encode,
    lambda x: x[::-1],
    RSA,
    rot13
]
flag = os.getenv('FLAG', 'ptm{ju57' + 'X' * (64 - 8 - 6) + 'tr1ck}').encode()
assert (
    flag.startswith(b'ptm{ju57')
    and flag.endswith(b'tr1ck}')
    and len(flag) == 64
)


if __name__ == '__main__':
    print('Hi challenger! I\'ll give you a flag encoded and encrypted with some magic methods that only the best cryptographers know!')
    print('If you want to get the flag, you will have to read the source code and try to invert all my special algorithms. I will give you the list of steps I have used and the result of all of them, good luck!')
    print()

    steps = []
    i = 0

    while i < 20:
        chosen = random.randint(0, len(possible_methods) - 1)

        if chosen == 2 and chosen in steps:
            # We don't want to use RSA twice
            continue
        steps.append(chosen)
        flag = possible_methods[chosen](flag)
        i += 1
    print(steps)
    print(flag.hex())
