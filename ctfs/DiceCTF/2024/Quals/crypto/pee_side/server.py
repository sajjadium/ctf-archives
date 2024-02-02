import sys

print("thinking...")
sys.stdout.flush()

from sage.all import *

# PSIDH class code is adapted from
# https://github.com/grhkm21/CTF-challenges/blob/master/Bauhinia-CTF-2023/Avengers/public/chasher.sage
proof.all(False)

x = var('x')

import random
import hashlib
class PSIDH:
    def __init__(self, l):
        self.n = len(l)
        self.l = l
        self.p = 4 * product(self.l) - 1
        assert is_prime(self.p)

        self.K = GF(self.p**2, modulus = x**2 + 1, names = 'i')
        self.i = self.K.gen(0)

        self.paramgen()

    def paramgen(self):
        E0 = EllipticCurve(self.K, [1, 0])

        # Move to random starting supersingular curve
        self.E0, _ = self.action(E0, E0(0), [random.randrange(-5, 6) for _ in ell])
        self.P0 = self.E0.random_point()

    def action(self, E, PP, priv):
        assert len(priv) == self.n
        
        E = EllipticCurve(self.K, E.ainvs())
        PP = E(PP)
        es = priv.copy()

        while any(es):
            E.set_order((self.p + 1)**2)
            
            P = E.lift_x(ZZ(randrange(self.p)))
            s = [-1, 1][P[1] in GF(self.p)]
            k = prod(l for l, e in zip(self.l, es) if sign(e) == s)
            P *= (self.p + 1) // k

            for i, (l, e) in enumerate(zip(self.l, es)):
                if sign(e) != s:
                    continue

                Q = k // l * P
                if not Q:
                    continue
                Q.set_order(l)
                psi = E.isogeny(Q)

                E, P, PP = psi.codomain(), psi(P), psi(PP)
                es[i] -= s
                k //= l
        
        return E, PP

    def to_secret(self, E, P):
        return hashlib.sha256((str(E.j_invariant()) + str(P.xy())).encode()).hexdigest()

if __name__ == '__main__':
    with open('flag.txt') as f:
        flag = f.read().strip()

    ell = list(prime_range(200, 450)) + [1483]
    psidh = PSIDH(ell)
    # Get the randomly generated public key
    E0, P0 = psidh.E0, psidh.P0
    
    a = [random.randrange(-1,2) for _ in ell]
    Ea, Pa = psidh.action(E0, P0, a)

    print(f'take this: ({Ea.ainvs()}, {Pa})')
    inp = input('something for me? ').strip()[2:-2].split('), (')

    try:
        Eb = EllipticCurve(psidh.K, [int(c) for c in inp[0].strip('()').split(', ')])
        assert Eb.is_supersingular()
        Pb = Eb([psidh.K(c) for c in inp[1].strip('()').split(', ')])
    except:
        print('tsk tsk tsk')
        exit()

    Eab, Pab = psidh.action(Eb, Pb, a)

    shared_secret = psidh.to_secret(Eab, Pab)

    guess = input('> ')
    if guess == shared_secret:
        print(flag)
    else:
        print('better luck next time...')