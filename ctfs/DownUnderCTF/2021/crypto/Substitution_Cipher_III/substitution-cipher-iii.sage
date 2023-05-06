def encrypt(pubkey, msg):
    gens = pubkey[0].parent().gens()
    n = len(gens)

    B = ''.join(f'{c:08b}' for c in msg)
    B = list(map(int, B))
    assert len(B) <= n
    B += [0] * (n - len(B))

    subs = { x: b for x, b in zip(gens, B) }
    return ''.join([str(p.substitute(subs)) for p in pubkey])

def generate_key(n):
    q = 2
    F = GF(q)
    K = BooleanPolynomialRing(n, 'x')
    R.<t> = PolynomialRing(K)
    i = GF(q)[t].irreducible_element(n)
    I = Ideal(R(i))
    I.reduce = lambda f: f % i # dirty sage hack
    E.<tbar> = PolynomialRing(K, t).quo(I)
    L.<x> = PolynomialRing(E)
    A = AffineGroup(n, K)

    S = A(GL(n, F).random_element(), random_vector(F, n), check=False)
    r = sum(randint(0, 1) * tbar^i for i in range(n))
    P = r * x^(q + 1)
    T = A(GL(n, F).random_element(), random_vector(F, n), check=False)

    B = S(K.gens()) * vector([tbar^i for i in range(n)])
    Q = P(B)
    R = T(Q.lift().coefficients())

    return R, (S, P, T)

pubkey, privkey = generate_key(80)

FLAG = open('./flag.txt', 'rb').read().strip()
assert FLAG.startswith(b'DUCTF{') and FLAG.endswith(b'}')
FLAG = FLAG.strip(b'DUCTF{}')
msg1 = FLAG[:10]
msg2 = FLAG[10:]

ct1 = encrypt(pubkey, msg1)
ct2 = encrypt(pubkey, msg2)

print(pubkey)
print(ct1)
print(ct2)
