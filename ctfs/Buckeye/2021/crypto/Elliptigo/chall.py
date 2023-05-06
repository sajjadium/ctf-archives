from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import size, long_to_bytes
import os
import hashlib
from collections import namedtuple

FLAG = b"buckeye{???????????????????}"

Point = namedtuple("Point", ("x", "z"))
Curve = namedtuple("Curve", ("a", "b"))

p = 2 ** 255 - 19
C = Curve(486662, 1)

"""
Implements the Montgomery Ladder from https://eprint.iacr.org/2017/212.pdf
"""


def point_add(P: Point, Q: Point, D: Point) -> Point:
    """
    Algorithm 1 (xADD)
    """
    V0 = (P.x + P.z) % p
    V1 = (Q.x - Q.z) % p
    V1 = (V1 * V0) % p
    V0 = (P.x - P.z) % p
    V2 = (Q.x + Q.z) % p
    V2 = (V2 * V0) % p
    V3 = (V1 + V2) % p
    V3 = (V3 * V3) % p
    V4 = (V1 - V2) % p
    V4 = (V4 * V4) % p
    x = (D.z * V3) % p
    z = (D.x * V4) % p
    return Point(x, z)


def point_double(P: Point) -> Point:
    """
    Algorithm 2 (xDBL)
    """
    V1 = (P.x + P.z) % p
    V1 = (V1 * V1) % p
    V2 = (P.x - P.z) % p
    V2 = (V2 * V2) % p
    x = (V1 * V2) % p
    V1 = (V1 - V2) % p
    V3 = (((C.a + 2) // 4) * V1) % p
    V3 = (V3 + V2) % p
    z = (V1 * V3) % p
    return Point(x, z)


def scalar_multiplication(P: Point, k: int) -> Point:
    """
    Algorithm 4 (LADDER)
    """

    if k == 0:
        return Point(0, 0)

    R0, R1 = P, point_double(P)
    for i in range(size(k) - 2, -1, -1):
        if k & (1 << i) == 0:
            R0, R1 = point_double(R0), point_add(R0, R1, P)
        else:
            R0, R1 = point_add(R0, R1, P), point_double(R1)
    return R0


def normalize(P: Point) -> Point:
    if P.z == 0:
        return Point(0, 0)

    return Point((P.x * pow(P.z, -1, p)) % p, 1)


def legendre_symbol(x: int, p: int) -> int:
    return pow(x, (p - 1) // 2, p)


def is_on_curve(x: int) -> bool:
    y2 = x ** 3 + C.a * x ** 2 + C.b * x
    return legendre_symbol(y2, p) != (-1 % p)


def main():
    print("Pick a base point")
    x = int(input("x: "))

    if size(x) < 245:
        print("Too small!")
        return

    if x >= p:
        print("Too big!")
        return

    if not is_on_curve(x):
        print("That x coordinate is not on the curve!")
        return

    P = Point(x, 1)

    a = int.from_bytes(os.urandom(32), "big")
    A = scalar_multiplication(P, a)
    A = normalize(A)

    key = hashlib.sha1(long_to_bytes(A.x)).digest()[:16]

    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    print(ciphertext.hex())


if __name__ == "__main__":
    main()
