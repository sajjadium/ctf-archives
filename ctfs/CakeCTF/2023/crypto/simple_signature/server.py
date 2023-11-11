import os
import sys
from hashlib import sha512
from Crypto.Util.number import getRandomRange, getStrongPrime, inverse, GCD
import signal


flag = os.environ.get("FLAG", "neko{cat_does_not_eat_cake}")

p = getStrongPrime(512)
g = 2


def keygen():
    while True:
        x = getRandomRange(2, p-1)
        y = getRandomRange(2, p-1)
        w = getRandomRange(2, p-1)

        v = w * y % (p-1)
        if GCD(v, p-1) != 1:
            continue
        u = (w * x - 1) * inverse(v, p-1) % (p-1)
        return (x, y, u), (w, v)


def sign(m, key):
    x, y, u = key
    r = getRandomRange(2, p-1)

    return pow(g, x*m + r*y, p), pow(g, u*m + r, p)


def verify(m, sig, key):
    w, v = key
    s, t = sig

    return pow(g, m, p) == pow(s, w, p) * pow(t, -v, p) % p


def h(m):
    return int(sha512(m.encode()).hexdigest(), 16)


if __name__ == '__main__':
    magic_word = "cake_does_not_eat_cat"
    skey, vkey = keygen()

    print(f"p = {p}")
    print(f"g = {g}")
    print(f"vkey = {vkey}")

    signal.alarm(1000)

    while True:
        choice = input("[S]ign, [V]erify: ").strip()
        if choice == "S":
            message = input("message: ").strip()
            assert message != magic_word

            sig = sign(h(message), skey)
            print(f"(s, t) = {sig}")

        elif choice == "V":
            message = input("message: ").strip()
            s = int(input("s: ").strip())
            t = int(input("t: ").strip())

            assert 2 <= s < p
            assert 2 <= t < p

            if not verify(h(message), (s, t), vkey):
                print("invalid signature")
                continue

            print("verified")
            if message == magic_word:
                print(f"flag = {flag}")
                sys.exit(0)

        else:
            break
