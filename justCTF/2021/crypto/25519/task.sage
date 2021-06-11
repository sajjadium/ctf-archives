#!/use/bin/env sage

from sys import exit
from hashlib import sha256


FLAG = open('./flag.txt').read()

ec = EllipticCurve(GF(2**255-19), [0, 486662, 0, 1, 0])
p = ec.order()
ZmodP = Zmod(p)
G = ec.lift_x(9)

ha = lambda x: x if isinstance(x, int) or isinstance(x, Integer) else product(x.xy())
hashs = lambda *x: int.from_bytes(sha256(b'.'.join([b'%X' % ha(x) for x in x])).digest(), 'little') % p


def hashp(x):
    x = hashs((x))
    while True:
        try:
            return ec.lift_x(x)
        except:
            x = hashs((x))


def keygen():
    x = randint(1, p-1)
    P = x * G
    return x, P


def verify(signature, P, m):
    I, e, s = signature
    return e == hashs(m, s*G + e*P, s*hashp(P) + e*I)


if __name__ == "__main__":
    x, P = keygen()
    m = randint(1, p-1)
    print(x, P, m)

    spent = set()
    for i in range(8):
        Ix = int(input('I (x): '))
        Iy = int(input('I (y): '))
        I = ec(Ix, Iy)
        e = int(input('e: '))
        s = int(input('s: '))
        if verify((I, e, s), P, m) and I not in spent:
            print('ok')
            spent.add(I)
        else:
            print('nope')
            exit(1)

    print(FLAG)
