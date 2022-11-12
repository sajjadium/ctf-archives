# The following imports are from the pycryptodome library
from Crypto.Util.number import isPrime, bytes_to_long
from functools import reduce
import random
import os


flag = os.getenv('FLAG', 'ptm{fake_flag}')


def getPrime() -> int:
    # Magic function to get 256 bits or more prime
    while True:
        p = random.randint(2, 2**16)
        ds = [int(d) for d in str(p)]
        r = reduce(lambda x, y: x * y, ds)

        if r in [1, 0]:
            continue

        while not isPrime(r) or r <= 2**256:
            r = r * 2 - 1
        return r


if __name__ == '__main__':
    p, q = getPrime(), getPrime()
    N = p * q
    e = 65537
    ciphertext = pow(bytes_to_long(flag.encode()), e, N)
    print('N =', N)
    print('ciphertext =', ciphertext)
