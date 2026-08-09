from sage.geometry.newton_polygon import NewtonPolygon

q, prec = 4, 800
k = GF(q^2, "c")
R = PuiseuxSeriesRing(k, "u", default_prec=prec)
u = R.gen()
T = u^-1
S.<A> = PolynomialRing(R)
B.<C> = PolynomialRing(k)


def _newton_lift(P, x, n=20):
    dP = P.derivative()
    for _ in range(n):
        y = P(x)
        if y.is_zero(): break
        x -= y / dP(x)
    return x.add_bigoh(prec)


def _puiseux_roots(P, lower=None, depth=0):
    if depth > P.degree() + prec: return []
    terms = [(i, c, QQ(c.valuation())) for i, c in enumerate(P) if not c.is_zero()]
    if not terms: return []

    roots = []
    V = NewtonPolygon([(i, v) for i, _, v in terms]).vertices()
    for (i0, v0), (i1, v1) in zip(V, V[1:]):
        v = -QQ(v1 - v0) / QQ(i1 - i0)
        if lower is not None and v <= lower: continue
        w = min(v0 + i*v for i, _, v0 in terms)
        residual = B.sum(k(c[c.valuation()])*C^i for i, c, v0 in terms if v0 + i*v == w)

        for lead, mult in residual.roots():
            if lead == 0: continue
            x0, branch = R(lead)*u^v, []

            def add(x):
                if all(not (x-y).is_zero() for y in branch): branch.append(x)

            if P(x0).is_zero(): add(x0.add_bigoh(prec))
            if mult == 1:
                try: add(_newton_lift(P, x0))
                except ZeroDivisionError: pass
            else:
                for dx in _puiseux_roots(P(A + x0), v, depth + 1):
                    if dx.is_zero() or dx.valuation() <= v: continue
                    x = x0 + dx
                    try: x = _newton_lift(P, x)
                    except ZeroDivisionError: x = x.add_bigoh(prec)
                    add(x)

            if len(branch) < mult:
                raise ValueError("not enough Puiseux precision to split branch")
            roots += branch[:mult]
            if len(roots) >= P.degree(): return roots
    return roots


def _target_g(g, a):
    return (g + a*(T^q - T))*a^(q - 1)


def j_invariant(g):
    return g^(q + 1)


def initial_edge():
    a = (u^(QQ(1)/(q + 1))).add_bigoh(prec)
    return _target_g(R.zero(), a), a


def forward_edges(g, previous_a, exclude_escape=False):
    back = 1/(T*previous_a)
    roots = _puiseux_roots(T*A^(q + 1) - g*A^q + 1)
    roots.pop(max(range(len(roots)), key=lambda i: (roots[i] - back).valuation()))
    edges = [(_target_g(g, a), a) for a in roots]
    if exclude_escape:
        edges.pop(min(range(len(edges)), key=lambda i: edges[i][0].valuation()))
    return edges


def _serialize_j(j):
    v = ZZ(j.valuation())
    return b",".join(f"{e}:{j[e]}".encode() for e in range(v, v + 12))
