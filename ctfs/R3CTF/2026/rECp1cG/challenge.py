from hashlib import sha256
from random import SystemRandom
from secrets import token_hex
import signal

from secret import flag


p_bits = 1024
k = 21
d_bits = 451
Delta = 1 << d_bits
solve_timeout = 888

rand = SystemRandom()


def is_prime(x):
    if x < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
             47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    for q in small:
        if x == q:
            return True
        if x % q == 0:
            return False

    odd = x - 1
    power = 0
    while odd % 2 == 0:
        odd //= 2
        power += 1

    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
             47, 53, 59, 61)
    for base in bases:
        if base % x == 0:
            continue
        y = pow(base, odd, x)
        if y == 1 or y == x - 1:
            continue
        for _ in range(power - 1):
            y = pow(y, 2, x)
            if y == x - 1:
                break
        else:
            return False
    return True


def make_prime(bits):
    while True:
        x = rand.getrandbits(bits)
        x |= 1 << (bits - 1)
        x |= 3
        if is_prime(x):
            return x


def add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        slope = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
    else:
        slope = (y2 - y1) * pow(x2 - x1, -1, p) % p

    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


def random_point(a, b, p):
    while True:
        x = rand.randrange(1, p)
        y2 = (x * x * x + a * x + b) % p
        if y2 != 0 and pow(y2, (p - 1) // 2, p) == 1:
            y = pow(y2, (p + 1) // 4, p)
            if rand.getrandbits(1):
                y = (-y) % p
            return x, y


def main():
    key_tag = token_hex(16)
    p = make_prime(p_bits)

    while True:
        a = rand.randrange(1, p)
        b = rand.randrange(1, p)
        if (4 * a * a * a + 27 * b * b) % p != 0:
            break

    while True:
        g = random_point(a, b, p)
        u = random_point(a, b, p)
        points = [u]
        for _ in range(k - 1):
            u = add(u, g, a, p)
            if u is None:
                break
            points.append(u)
        if len(points) == k and len({P[0] for P in points}) == k:
            break

    states = []
    for x, _ in points:
        while True:
            shown = x - rand.randrange(-Delta, Delta + 1)
            if 0 <= shown < p:
                states.append(shown)
                break

    size = (p.bit_length() + 7) // 8
    nums = (a, b, g[0], g[1], points[0][0], points[0][1])
    material = b"".join(int(x).to_bytes(size, "big") for x in nums)
    key = sha256(material + b"|" + key_tag.encode()).digest()

    pad = b""
    ctr = 0
    while len(pad) < len(flag):
        pad += sha256(key + ctr.to_bytes(4, "big")).digest()
        ctr += 1
    ct = bytes(x ^ y for x, y in zip(flag, pad)).hex()

    print(f"p = {p}")
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"Delta = {Delta}")
    print(f"G = {g}")
    print(f"states = {states}")
    print()
    print("# submit P0.x", flush=True)

    signal.alarm(solve_timeout)
    try:
        answer = input().strip()
    except EOFError:
        return

    if len(answer) > 4096:
        print("# wrong", flush=True)
        return

    try:
        recovered_x = int(answer, 0)
    except ValueError:
        print("# wrong", flush=True)
        return

    if recovered_x != points[0][0]:
        print("# wrong", flush=True)
        return

    print("# ok", flush=True)
    print(f"key_tag = {key_tag!r}")
    print(f"ct = {ct!r}", flush=True)


if __name__ == "__main__":
    main()
