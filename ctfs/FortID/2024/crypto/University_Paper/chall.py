from Crypto.Util.number import *
from redacted import FLAG

ESSAY_TEMPLATE = """
On the Estemeed Scientifc Role Model of Mine
============================================

Within the confines of this academic setting, the individual whom
I hold in highest regard not only boasts an engaging smile but also
possesses a remarkable sense of humor, complemented by an array of
vibrant notebooks.

Yet, it is their distinct quantifiable attribute that stands out
most prominently: their name, when converted into an integer value
and squared modulo %d,
astonishingly results in %d.

Furthermore, the greatest integer that does not surpass the cube root
of the aforementioned squared name equals %d.
This computational detail adds another layer of distinction.

It is likely that by this point, many of you have discerned the identity
of this distinguished role model.
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


N = 13113180816763040887576781992067364636289723584543479342139964290889855987378109190372819034517913477911738026253141916115785049387269347257060732629562571

name_int = bytes_to_long(FLAG)

assert 1 < name_int < N

value_1 = (name_int**2) % N
value_2 = invpow3(name_int**2)

assert (value_2**3) <= (name_int**2)
assert ((value_2 + 2) ** 3) > (name_int**2)

print(ESSAY_TEMPLATE % (N, value_1, value_2))
