#!/usr/bin/env python3
import os
import secrets
from math import gcd

# Public generator template (safe to share)
BITS = 2048
E = 17
DEGREE = 9
POINTS = 10
X_BITS = 256
COEFF_BITS = 256
NOISE_BITS = 16


def is_probable_prime(n, k=40):
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_prime(bits):
    while True:
        n = secrets.randbits(bits)
        n |= (1 << (bits - 1)) | 1
        if is_probable_prime(n):
            return n


def poly_eval_mod(coeffs, x, n):
    acc = 0
    for c in coeffs:
        acc = (acc * x + c) % n
    return acc


def main():
    flag = os.environ.get("FLAG", "flag{placeholder}").encode()
    m = int.from_bytes(flag, "big")
    if m == 0:
        raise SystemExit("FLAG vuota")

    while True:
        p = gen_prime(BITS // 2)
        q = gen_prime(BITS // 2)
        if p == q:
            continue
        n = p * q
        if m >= n:
            continue

        coeffs = [secrets.randbits(COEFF_BITS) for _ in range(DEGREE + 1)]
        if coeffs[0] == 0:
            coeffs[0] = 1
        if gcd(coeffs[0], n) != 1:
            continue

        points = []
        xs = []
        while len(points) < POINTS:
            x = secrets.randbits(X_BITS)
            if x == 0 or gcd(x, n) != 1:
                continue
            if any(gcd(x - xj, n) != 1 for xj in xs):
                continue
            xs.append(x)

            y = poly_eval_mod(coeffs, x, n)
            r = secrets.randbelow(1 << NOISE_BITS)
            y_noisy = (y + r) % n
            r_enc = pow(r, E, n)
            points.append((x, y_noisy, r_enc))

        f_m = poly_eval_mod(coeffs, m, n)
        if gcd(f_m, n) != 1:
            continue

        c1 = pow(m, E, n)
        c2 = pow(f_m, E, n)
        break

    out = [
        f"n = {n}",
        f"e = {E}",
        f"deg = {DEGREE}",
        f"noise_bits = {NOISE_BITS}",
        f"c1 = {c1}",
        f"c2 = {c2}",
    ]

    secrets.SystemRandom().shuffle(points)
    for idx, (x, y, r_enc) in enumerate(points, 1):
        out.append(f"x{idx} = {x}")
        out.append(f"y{idx} = {y}")
        out.append(f"r{idx} = {r_enc}")

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
