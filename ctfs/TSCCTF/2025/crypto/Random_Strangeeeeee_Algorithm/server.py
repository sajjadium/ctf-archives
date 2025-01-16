import os
import random
import sys
from Crypto.Util.number import getRandomNBitInteger, bytes_to_long
from gmpy2 import is_prime
from secret import FLAG


def get_prime(nbits: int):
    if nbits < 2:
        raise ValueError("'nbits' must be larger than 1.")
    
    while True:
        num = getRandomNBitInteger(nbits) | 1
        if is_prime(num):
            return num


def pad(msg: bytes, nbytes: int):
    if nbytes < (len(msg) + 1):
        raise ValueError("'nbytes' must be larger than 'len(msg) + 1'.")

    return msg + b'\0' + os.urandom(nbytes - len(msg) - 1)


def main():
    for cnt in range(4096):
        nbits_0 = 1000 + random.randint(1, 256)
        nbits_1 = 612 + random.randint(1, 256)

        p, q, r = get_prime(nbits_0), get_prime(nbits_0), get_prime(nbits_0)
        n = p * q * r
        d = get_prime(nbits_1)
        e = pow(d, -1, (p - 1) * (q - 1) * (r - 1))

        m = bytes_to_long(pad(FLAG, (n.bit_length() - 1) // 8))
        c = pow(m, e, n)

        print(f'{n, e = }')
        print(f'{c = }')
        msg = input('Do you want to refresh [Y/N] > ')
        if msg != 'Y':
            break


if __name__ == '__main__':
    try:
        main()
    except Exception:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()
