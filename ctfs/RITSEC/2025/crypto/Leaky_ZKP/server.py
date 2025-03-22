#!/usr/local/bin/python

from os import urandom, getenv
from secrets import randbelow
from Crypto.Util.number import getPrime, bytes_to_long

FLAG = getenv('FLAG', 'MetaCTF{test_flag}').encode()

def main():
    p = getPrime(512)
    k = 32
    x = bytes_to_long(FLAG + urandom(64 - len(FLAG)))
    g = 3
    h = pow(g, x, p)

    print('Let me prove to you in *zero-knowledge* that I know the discrete log of h!')
    print(f'{p = }')
    print(f'{g = }')
    print(f'{h = }')

    # 1. Prover (me) chooses random r_i for i = 1, 2, ..., k and sends each g^r_i
    R = [randbelow(p) for _ in range(k)]
    print([pow(g, r_i, p) for r_i in R])

    # 2. Verifier (you) chooses and sends random bits b_i for i = 1, 2, ..., k
    B = [int(b_i) for b_i in input(f'Send b_1, b_2, ..., b_{k}: ').split(',')]
    assert len(B) == k and all(b_i >= 0 for b_i in B)

    # 3. Prover (me) computes z_i = r_i + b_i x for i = 1, 2, ..., k and sends each z_i
    Z = [r_i + b_i * x for r_i, b_i in zip(R, B)]
    print(Z)

    # 4. Verifier (you) has sufficient information to be convinced that I truly know the discrete log!
    print('With that, you can verify that I know the discrete log, and you will have learnt nothing about my secret!')

if __name__ == '__main__':
    main()
