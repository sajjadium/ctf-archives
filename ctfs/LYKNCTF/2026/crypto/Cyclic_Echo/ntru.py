from __future__ import annotations


def _trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _deg(a):
    a = _trim(a)
    return len(a) - 1 if a != [0] else -1


def _padd(a, b, q):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(len(a)):
        out[i] = (out[i] + a[i]) % q
    for i in range(len(b)):
        out[i] = (out[i] + b[i]) % q
    return _trim(out)


def _psub(a, b, q):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(len(a)):
        out[i] = (out[i] + a[i]) % q
    for i in range(len(b)):
        out[i] = (out[i] - b[i]) % q
    return _trim(out)


def _pmul(a, b, q):
    if a == [0] or b == [0]:
        return [0]
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % q
    return _trim(out)


def _pdivmod(a, b, q):
    a = _trim(a)
    b = _trim(b)
    db = _deg(b)
    if db < 0:
        raise ZeroDivisionError("error")
    inv_lead = pow(b[db], q - 2, q)
    rem = list(a)
    quot = [0] * max(1, len(a) - db)
    while True:
        rem = _trim(rem)
        dr = _deg(rem)
        if dr < db:
            break
        coeff = (rem[dr] * inv_lead) % q
        shift = dr - db
        quot[shift] = (quot[shift] + coeff) % q
        # rem -= coeff * x^shift * b
        sub = [0] * shift + [(coeff * bc) % q for bc in b]
        rem = _psub(rem, sub, q)
    return _trim(quot), _trim(rem)


def _egcd_poly(a, b, q):
    old_r, r = _trim(a), _trim(b)
    old_s, s = [1], [0]
    old_t, t = [0], [1]
    while _deg(r) >= 0 and r != [0]:
        quot, rem = _pdivmod(old_r, r, q)
        old_r, r = r, rem
        old_s, s = s, _psub(old_s, _pmul(quot, s, q), q)
        old_t, t = t, _psub(old_t, _pmul(quot, t, q), q)
    return _trim(old_r), _trim(old_s), _trim(old_t)


def poly_mul_mod(a, b, N, q):
    out = [0] * N
    for i in range(N):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(N):
            out[(i + j) % N] = (out[(i + j) % N] + ai * b[j]) % q
    return out


def poly_eval_one(a, q):
    return sum(a) % q


def poly_inverse_cyclic(f, N, q):
    mod_poly = [(-1) % q] + [0] * (N - 1) + [1]  # x^N - 1
    g, s, _t = _egcd_poly(f, mod_poly, q)
    if _deg(g) != 0:
        return None
    inv_lead = pow(g[0], q - 2, q)
    s = [(c * inv_lead) % q for c in s]
    s = (s + [0] * N)[:N]
    return s


def center(a, q):
    return [(c - q) if c > q // 2 else c for c in a]
