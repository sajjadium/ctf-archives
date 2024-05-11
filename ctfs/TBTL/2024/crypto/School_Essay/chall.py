from Crypto.Util.number import *
from redacted import FLAG

ESSAY_TEMPLATE = """
My Favorite Classmate
=====================

My favorite person in this class has a beautiful smile,
great sense of humour, and lots of colorful notebooks.

However, their most distinctive feature is the fact that
you can represent their name as an integer value, square
it modulo %d,
and you'll get %d.

Additionally, When you compute the greatest integer not exceeding
the cube root of their squared name, you get %d.

By now, all of you have probably guessed who I'm talking about.
"""


def invpow3(x):
    lo, hi = 1, x
    while lo < hi:
        mid = (lo + hi) // 2 + 1
        if (mid**3) <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


N = 59557942237937483757629838075432240015613811860811898821186897952866236010569299041278104165604573

name_int = bytes_to_long(FLAG)

assert 1 < name_int < N

value_1 = (name_int**2) % N
value_2 = invpow3(name_int**2)

print(ESSAY_TEMPLATE % (N, value_1, value_2))
