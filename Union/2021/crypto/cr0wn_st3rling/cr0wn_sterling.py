#!/usr/bin/env python3

from secrets import flag, musical_key
from Crypto.Util.number import isPrime
import math


def sieve_for_primes_to(n):
    # Copyright Eratosthenes, 204 BC
    size = n//2
    sieve = [1]*size
    limit = int(n**0.5)
    for i in range(1, limit):
        if sieve[i]:
            val = 2*i+1
            tmp = ((size-1) - i)//val
            sieve[i+val::val] = [0]*tmp
    return [2] + [i*2+1 for i, v in enumerate(sieve) if v and i > 0]


def is_quasi_prime(n, primes):
    # novel class of semi-prime numbers
    # https://arxiv.org/pdf/1903.08570.pdf
    p2 = 0
    for p1 in primes:
        if n % p1 == 0:
            p2 = n//p1
            break
    if isPrime(p2) and not p1 in [2, 3] and not p2 in [2, 3]:
        return True
    return False


def bbp_pi(n):
    # Bailey-Borwein-Plouffe Formula
    # sounds almost as cool as Blum-Blum-Shub
    # nth hex digit of pi
    def S(j, n):
        s = 0.0
        k = 0
        while k <= n:
            r = 8*k+j
            s = (s + pow(16, n-k, r) / r) % 1.0
            k += 1
        t = 0.0
        k = n + 1
        while 1:
            newt = t + pow(16, n-k) / (8*k+j)
            if t == newt:
                break
            else:
                t = newt
            k += 1
        return s + t

    n -= 1
    x = (4*S(1, n) - 2*S(4, n) - S(5, n) - S(6, n)) % 1.0
    return "%02x" % int(x * 16**2)


def digital_root(n):
    # reveals Icositetragon modalities when applied to Fibonacci sequence
    return (n - 1) % 9 + 1 if n else 0


def fibonacci(n):
    # Nature's divine proportion gives high-speed oscillations of infinite
    # wave values of irrational numbers
    assert(n >= 0)
    if n < digital_root(2):
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def is_valid_music(music):
    # Leverage music's infinite variability
    assert(all(c in "ABCDEFG" for c in music))


def is_valid_number(D):
    # Checks if input symbolizes the digital root of oxygen
    assert(8==D)


def get_key(motif):
    is_valid_music(motif)
    is_valid_number(len(motif))
    # transpose music onto transcendental frequencies
    indexes = [(ord(c)-0x40)**i for i, c in enumerate(motif)]
    size = sum(indexes)
    assert(size < 75000) # we will go larger when we have quantum
    return indexes, size


def get_q_grid(size):
    return [i for i in range(size) if is_quasi_prime(i, sieve_for_primes_to(math.floor(math.sqrt(size))+1))]


if __name__ == "__main__":
    print("[+] Oscillating the key")
    key_indexes, size = get_key(musical_key)
    print("[+] Generating quasi-prime grid")
    q_grid = get_q_grid(size)
    # print(f"indexes: {key_indexes}  size: {size}  len(q_grid): {len(q_grid)}")

    out = []
    for i, p in enumerate(flag):
        print(f"[+] Entangling key and plaintext at position {i}")
        index = key_indexes[i % len(key_indexes)] * fibonacci(i)
        q = q_grid[index % len(q_grid)]
        key_byte_hex = bbp_pi(q)
        # print(f"index: {index:10}  fib: {fibonacci(i):10}  q-prime: {q:10}  keybyte: {key_byte_hex:10}")
        out.append(ord(p) ^ int(key_byte_hex, 16))

    print(f"[+] Encrypted: {bytes(out).hex()}")
