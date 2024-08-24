from random import randint

# I received advice from Mitsu to write this program. I appreciate it very much

def montgomery(Fp2, A):
    return EllipticCurve(Fp2, [0, A, 0, 1, 0])

def to_montgomery(Fp, Fp2, E, G):
    Ep = E.change_ring(Fp).short_weierstrass_model()
    a, b = Ep.a4(), Ep.a6()
    P.<x> = PolynomialRing(Fp)
    r = (x^3 + a*x + b).roots()[0][0]
    s = sqrt(3 * r^2 + a)
    if not is_square(s):
        s = -s
    A = 3 * r / s
    phi = E.isomorphism_to(EllipticCurve(Fp2, [0, A, 0, 1, 0]))
    return Fp(A), phi(G)

def group_action(p, primes, Fp, Fp2, pub, priv, G):
    E = montgomery(Fp2, pub)
    es = priv[:]
    while any(es):
        x = Fp.random_element()
        P = E.lift_x(x)
        s = 1 if P[1] in Fp else -1
        S = [i for i, e in enumerate(es) if sign(e) == s and e != 0]
        k = prod([primes[i] for i in S])
        Q = ((p + 1) // k) * P
        
        for i in S:
            R = (k // primes[i]) * Q
            if R.is_zero():
                continue
            phi = E.isogeny(R)
            E = phi.codomain()
            Q, G = phi(Q), phi(G)
            es[i] -= s
            k //= primes[i]
    return to_montgomery(Fp, Fp2, E, G)
