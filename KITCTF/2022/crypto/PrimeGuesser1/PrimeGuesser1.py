#!/usr/bin/env python3

import numpy as np
from numpy.polynomial import polynomial as poly
import random

def polymul(x, y, modulus, poly_mod):
    return np.int64(
        np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus)
    )


def polyadd(x, y, modulus, poly_mod):
    return np.int64(
        np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus)
    )

def gen_binary_poly(size):
    return np.random.randint(0, 2, size, dtype=np.int64)


def gen_uniform_poly(size, modulus):
    return np.random.randint(0, modulus, size, dtype=np.int64)


def gen_normal_poly(size):
    return np.int64(np.random.normal(0, 2, size=size))

def keygen(size, modulus, poly_mod):
    sk = gen_binary_poly(size)
    a = gen_uniform_poly(size, modulus)
    e = gen_normal_poly(size)
    b = polyadd(polymul(-a, sk, modulus, poly_mod), -e, modulus, poly_mod)
    return (b, a), sk

def encrypt(pk, size, q, t, poly_mod, pt):
    m = np.array([pt] + [0] * (size - 1), dtype=np.int64) % t
    delta = q // t
    scaled_m = delta * m  % q
    e1 = gen_normal_poly(size)
    e2 = gen_normal_poly(size)
    u = gen_binary_poly(size)
    ct0 = polyadd(
            polyadd(
                polymul(pk[0], u, q, poly_mod),
                e1, q, poly_mod),
            scaled_m, q, poly_mod
        )
    ct1 = polyadd(
            polymul(pk[1], u, q, poly_mod),
            e2, q, poly_mod
        )
    return (ct0, ct1)


def decrypt(sk, size, q, t, poly_mod, ct):
    scaled_pt = polyadd(
            polymul(ct[1], sk, q, poly_mod),
            ct[0], q, poly_mod
        )
    decrypted_poly = np.round(scaled_pt * t / q) % t
    return int(decrypted_poly[0])

def get_factors(number):
    factors = set()
    for i in [2, 3, 5, 7, 11, 13, 15, 17, 19, 23]:
        if i >= number:
            break
        if (number % i == 0):
            factors.add(i)
            other = number // i
            prime_set = get_factors(other)
            if len(prime_set) == 0:
                factors.add(other)
            else:
                for num in prime_set:
                    factors.add(num)
            
    return factors

# polynomial modulus degree
n = 2**6 # EXAMPLE !!! ON THE SERVER ARE OTHER NUMBERS
# ciphertext modulus
q = 2**20 # EXAMPLE !!! ON THE SERVER ARE OTHER NUMBERS
# plaintext modulus
t = 2**10 # EXAMPLE !!! ON THE SERVER ARE OTHER NUMBERS
# polynomial modulus
poly_mod = np.array([1] + [0] * (n - 1) + [1])
pk, sk = keygen(n, q, poly_mod)


def oracle(c):
    p = decrypt(sk, n, q, t, poly_mod, c)
    print(p == 0)

def smart_enrypt(p):
    if p > 0 and p < 25:
        return encrypt(pk, n, q, t, poly_mod, p)

def loose():
    print("Failed")
    exit()

def outputCipher(c):
    print(''.join([str(l) + "," for l in c[0]])[:-1])
    print(''.join([str(l) + "," for l in c[1]])[:-1])

for _ in range(100):
    number = random.randint(11, 200)
    
    ct = encrypt(pk, n, q, t, poly_mod, number)
    outputCipher(ct)
    while True:
        choice = int(input("What do you want?\n").strip())
        if choice == 0:
            number_input = int(input("What do you want to encrypt?\n").strip(), 10)
            if number_input > 20 or number_input < 1:
                print("Thats out of bound")
            else:
                outputCipher(smart_enrypt(number_input))
        elif choice == 1:
            cipher_input = input("What is the first part of the Cipher?\n").strip()
            c0 = [int(n, 10) for n in cipher_input.split(",")]
            cipher_input = input("What is the second part of the Cipher?\n").strip()
            c1 = [int(n, 10) for n in cipher_input.split(",")]
            c = (c0, c1)
            oracle(c)
        elif choice == 2:
            break
    
    real_factors = get_factors(number)
    primes = input("What are the factors?\n").strip()
    if len(primes) == 0:
        if len(real_factors) == 0:
            continue
        else:
            loose()

    primes_set = set()
    for num in primes.split(","):
        primes_set.add(int(num, 10))
    
    if not (real_factors == primes_set):
        loose()

print("You won: Flag")