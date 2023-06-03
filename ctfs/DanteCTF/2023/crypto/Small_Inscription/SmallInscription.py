#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, getPrime
from secret import FLAG

assert len(FLAG) < 30

if __name__ == '__main__':

    msg = bytes_to_long(
        b'There is something reeeally important you should know, the flag is '+FLAG)
    N = getPrime(1024)*getPrime(1024)
    e = 3

    ct = pow(msg, e, N)
    print(f'{ct=}')
    print(f'{N=}')
