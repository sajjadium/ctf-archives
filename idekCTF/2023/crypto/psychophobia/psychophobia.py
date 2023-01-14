#!/usr/bin/env python3
#
# Polymero
#

# Imports
from Crypto.Util.number import inverse
from secrets import randbelow
from hashlib import sha256

# Local imports
with open('flag.txt', 'rb') as f:
    FLAG = f.read()
    f.close()

# Header
HDR = r"""|
|                                _           ___
|                               | |         / _ \
|    _  _  _ _   ___   _____   _| |_   ___ | |_) )_  __  __
|   | || || | | | \ \ / / _ \ /     \ / _ \|  _ <| |/  \/ /
|   | \| |/ | |_| |\ v ( (_) | (| |) | (_) ) |_) ) ( ()  <
|    \_   _/ \___/  > < \___/ \_   _/ \___/|  __/ \_)__/\_\
|      | |         / ^ \        | |        | |
|      |_|        /_/ \_\       |_|        |_|
|
|"""


# Curve 25519 :: By^2 = x^3 + Ax^2 + x  mod P
# https://en.wikipedia.org/wiki/Curve25519
# Curve Parameters
P = 2**255 - 19
A = 486662
B = 1
# Order of the Curve
O = 57896044618658097711785492504343953926856930875039260848015607506283634007912

# ECC Class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if not self.is_on_curve():
            raise ValueError("Point NOT on Curve 25519!")

    def is_on_curve(self):
        if self.x == 0 and self.y == 1:
            return True
        if ((self.x**3 + A * self.x**2 + self.x) % P) == ((B * self.y**2) % P):
            return True
        return False

    @staticmethod
    def lift_x(x):
        y_sqr = ((x**3 + A * x**2 + x) * inverse(B, P)) % P
        v = pow(2 * y_sqr, (P - 5) // 8, P)
        i = (2 * y_sqr * v**2) % P
        return Point(x, (y_sqr * v * (1 - i)) % P)

    def __repr__(self):
        return "Point ({}, {}) on Curve 25519".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if self == self.__class__(0, 1):
            return other
        if other == self.__class__(0, 1):
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(0, 1)

        if self.x != other.x:
            l = ((other.y - self.y) * inverse(other.x - self.x, P)) % P
        else:
            l = ((3 * self.x**2 + 2 * A * self.x + 1) * inverse(2 * self.y, P)) % P

        x3 = (l**2 - A - self.x - other.x) % P
        y3 = (l * (self.x - x3) - self.y) % P
        return self.__class__(x3, y3)

    def __rmul__(self, k):
        out = self.__class__(0, 1)
        tmp = self.__class__(self.x, self.y)
        while k:
            if k & 1:
                out += tmp
            tmp += tmp
            k >>= 1
        return out

# Curve25519 Base Point
G = Point.lift_x(9)


# ECDSA Functions
# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
def ECDSA_sign(m, priv):
    h = int.from_bytes(sha256(m.encode()).digest(), 'big')
    k = (4 * randbelow(O)) % O
    r = (k * G).x % O
    s = (inverse(k, O) * (h + r * priv)) % O
    return (r, s)

def ECDSA_verify(m, pub, sig):
    r, s = sig
    if r > 0 and r < O and s > 0 and s < O:
        h = int.from_bytes(sha256(m.encode()).digest(), 'big')
        u1 = (h * inverse(s, O)) % O
        u2 = (r * inverse(s, O)) % O
        if r == (u1 * G + u2 * pub).x % O:
            return True
    return False


# Server connection
print(HDR)

print("|\n|  ~ Are you the psychic I requested? What can I call you?")
name = input("|    > ")

msg = f"{name} here, requesting flag for pick-up."
print('|\n|  ~ Alright, here is the message I will sign for you :: ')
print(f'|    m = \"{msg}\"')

ITER = 500
RATE = 0.72
print(f'|\n|  ~ The following {ITER} signatures are all broken, please fix them for me to prove your psychic abilities ~')
print(f'|    If you get more than, say, {round(RATE * 100)}% correct, I will believe you ^w^')


# Server loop
success = 0
for k in range(ITER):

    try:

        d = (2 * randbelow(O) + 1) % O
        Q = d * G

        while True:
            sig = ECDSA_sign(msg, d)
            if not ECDSA_verify(msg, Q, sig):
                break

        print(f"|\n|  {k}. Please fix :: {sig}")

        fix = [int(i.strip()) for i in input("|    > (r,s) ").split(',')]

        if (sig[0] == fix[0]) and ECDSA_verify(msg, Q, fix):
            success += 1

    except KeyboardInterrupt:
        print('\n|')
        break

    except:
        continue

print(f"|\n|  ~ You managed to fix a total of {success} signatures!")

if success / ITER > RATE:
    print(f"|\n|  ~ You truly are psychic, here {FLAG}")
else:
    print("|\n|  ~ Seems like you are a fraud after all...")

print('|\n|')