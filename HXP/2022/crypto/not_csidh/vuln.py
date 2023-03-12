#!/usr/bin/env python3
from sage.all import *
proof.all(False)

p = 0x196c20a5235aa2c43071905be8e809d089d24fa9144143cf0977680f15b11351
j = 0x145b6a85f73443b1ef971b5152d87725ffe78a542bcaf60671e7afa3857a2530
ls = [3, 5, 7, 11, 13, 19, 23, 31, 71, 89, 103, 109, 113, 131, 149, 151, 163, 179, 193, 211, 223, 233]
B = 20

################################################################

def not_csidh(pub, priv):

    E = EllipticCurve(GF(p), j=pub)
    if E.order() > p:
        E = E.quadratic_twist()
    n = E.order()

    es = list(priv)
    assert all(e >= 0 for e in es)

    while any(es):
        js = [j for j,e in enumerate(es) if e]
        if __name__ == '__main__':
            print(f'[{",".join(str(e).rjust(2) for e in es)}]', file=sys.stderr)

        k = prod(ls[j] for j in js)
        P = E.random_point()
        P *= n // k

        for j in js[:]:
            k //= ls[j]
            Q = k * P

            if Q:
                Q.set_order(ls[j])
                algo = (None, 'velusqrt')[Q.order() > 999]
                phi = E.isogeny(Q, algorithm=algo)
                E,P = phi.codomain(), phi(P)
                es[j] -= 1

    return ZZ(E.j_invariant())

################################################################

class NotCSIDH:
    def __init__(self):
        randrange = __import__('random').SystemRandom().randrange
        self.priv = tuple(randrange(B+1) for _ in ls)
        self.pub = not_csidh(j, self.priv)
    def public(self): return self.pub
    def shared(self, other): return not_csidh(other, self.priv)

################################################################

if __name__ == '__main__':

    alice = NotCSIDH()
    print('alice:', hex(alice.public()))

    bob = NotCSIDH()
    print('bob:', hex(bob.public()))

    shared, = {alice.shared(bob.public()),
               bob.shared(alice.public())}

    from Crypto.Hash import SHA512
    stream = SHA512.new(hex(shared).encode()).digest()
    flag = open('flag.txt','rb').read().strip()
    assert len(flag) <= len(stream)
    print('flag:', bytes(x^y for x,y in zip(flag,stream)).hex())

