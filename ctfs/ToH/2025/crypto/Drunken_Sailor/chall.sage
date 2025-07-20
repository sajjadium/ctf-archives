proof.all(False)

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 587]

p = 4*prod(PRIMES) - 1
max_exp = 20
N_PRIMES = 6
CSIDH_PRIMES = PRIMES[:N_PRIMES]

Fp = GF(p)
Fp2.<w> = GF(p**2, modulus = x**2 + 1)
E0 = EllipticCurve(Fp2, [1,0])

def action(pub, priv):
    E = pub
    es = priv[:]
    while any(es):
        E._order = (p + 1)**2 # else sage computes this
        P = E.lift_x(GF(p).random_element())
        s = +1 if P.xy()[1] in GF(p) else -1
        k = prod(l for l, e in zip(CSIDH_PRIMES, es) if sign(e) == s)
        P *= (p + 1) // k
        for i, (l, e) in enumerate(zip(CSIDH_PRIMES, es)):
            if sign(e) != s: continue
            Q = k // l * P
            if not Q: continue
            Q._order = l # else sage computes this
            phi = E.isogeny(Q)
            E, P = phi.codomain(), phi(P)
            es[i] -= s
            k //= l
    return E

def keygen():
    return [randrange(-max_exp, max_exp + 1) for _ in range(len(CSIDH_PRIMES))]

if __name__ == "__main__":
    alice_secret = keygen()
    EA = E0

    # Faster CSIDH
    while any(alice_secret):
        EA._order = (p+1)**2 # else sage computes this
        k = prod(l for l, e in zip(CSIDH_PRIMES, alice_secret) if e != 0)
        while True:
            P = EA.lift_x(Fp.random_element())
            P *= (p+1) // k
            if P:
                break
        for i, ell in enumerate(CSIDH_PRIMES):
            if alice_secret[i] == 0:
                continue
            s = sign(alice_secret[i])
            Q = (k // ell) * P
            if not Q:
                continue
            Q._order = ell
            phi = EA.isogeny(Q)
            EA, P = phi.codomain(), phi(P)
            alice_secret[i] -= s
            k //= ell

    print(f'j = {EA.j_invariant()}')
    print(f'Insert alice secret: ')
    sec = [int(_) for _ in input().split(',')]
    assert len(sec) == len(CSIDH_PRIMES)
    assert all(i <= max_exp for i in sec)
    EB = action(E0, sec)
    if EB.j_invariant() == EA.j_invariant():
        with open('flag.txt') as fh:
            print(fh.read())

