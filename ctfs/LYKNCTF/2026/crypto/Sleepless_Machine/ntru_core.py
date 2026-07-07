import random


def poly_trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_add(a, b, mod=None):
    n = max(len(a), len(b))
    r = [0] * n
    for i, x in enumerate(a):
        r[i] += x
    for i, x in enumerate(b):
        r[i] += x
    if mod:
        r = [x % mod for x in r]
    return poly_trim(r)


def poly_sub(a, b, mod=None):
    n = max(len(a), len(b))
    r = [0] * n
    for i, x in enumerate(a):
        r[i] += x
    for i, x in enumerate(b):
        r[i] -= x
    if mod:
        r = [x % mod for x in r]
    return poly_trim(r)


def poly_scale(a, c, mod=None):
    r = [x * c for x in a]
    if mod:
        r = [x % mod for x in r]
    return poly_trim(r)


def poly_mul(a, b, mod=None):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            r[i + j] += ai * bj
    if mod:
        r = [x % mod for x in r]
    return poly_trim(r)


def poly_divmod(a, b, mod):
    a = poly_trim(list(a))
    b = poly_trim(list(b))
    db = len(b) - 1
    inv_lead = pow(b[-1], mod - 2, mod)
    if len(a) - 1 < db:
        return [0], a
    q = [0] * (len(a) - db)
    while len(a) - 1 >= db and a != [0]:
        da = len(a) - 1
        coeff = (a[-1] * inv_lead) % mod
        shift = da - db
        q[shift] = (q[shift] + coeff) % mod
        for i, bc in enumerate(b):
            a[i + shift] = (a[i + shift] - coeff * bc) % mod
        a = poly_trim(a)
    return poly_trim(q), poly_trim(a)


def egcd_poly(a, b, mod):
    old_r, r = poly_trim(list(a)), poly_trim(list(b))
    old_s, s = [1], [0]
    old_t, t = [0], [1]
    while r != [0]:
        qq, rem = poly_divmod(old_r, r, mod)
        old_r, r = r, rem
        old_s, s = s, poly_sub(old_s, poly_mul(qq, s, mod), mod)
        old_t, t = t, poly_sub(old_t, poly_mul(qq, t, mod), mod)
    return old_r, old_s, old_t


def poly_mod_cyclic(a, N, mod=None):
    r = [0] * N
    for i, c in enumerate(a):
        r[i % N] += c
    if mod:
        r = [x % mod for x in r]
    return r


def poly_mul_cyclic(a, b, N, mod=None):
    return poly_mod_cyclic(poly_mul(a, b, mod), N, mod)


def invert_mod_q(f, N, q):
    mod_poly = [(-1) % q] + [0] * (N - 1) + [1]  # x^N - 1
    f_padded = poly_trim(list(f))
    g, u, v = egcd_poly(f_padded, mod_poly, q)
    if len(g) != 1 or g[0] == 0:
        raise ValueError("polynomial is not invertible mod q")
    inv_scale = pow(g[0], q - 2, q)
    u_scaled = poly_scale(u, inv_scale, q)
    return poly_mod_cyclic(u_scaled, N, q)


def sum_even_odd(poly, N):
    se = sum(poly[i] for i in range(0, N, 2))
    so = sum(poly[i] for i in range(1, N, 2))
    return se, so


def constrained_ternary(N, target_even, target_odd, density, rng):
    even_idx = list(range(0, N, 2))
    odd_idx = list(range(1, N, 2))
    poly = [0] * N

    def place(indices, target):
        pos = indices[:]
        rng.shuffle(pos)
        n_pos = max(target, 0)
        n_neg = max(-target, 0)
        it = iter(pos)
        used = []
        for _ in range(n_pos):
            i = next(it)
            poly[i] = 1
            used.append(i)
        for _ in range(n_neg):
            i = next(it)
            poly[i] = -1
            used.append(i)
        return [i for i in pos if i not in used]

    rem_even = place(even_idx, target_even)
    rem_odd = place(odd_idx, target_odd)

    used_count = sum(1 for c in poly if c != 0)
    target_total = int(density * N)
    pad_needed = max(target_total - used_count, 0)

    def pad(remaining, pairs_needed):
        rng.shuffle(remaining)
        i, made = 0, 0
        while made < pairs_needed and i + 1 < len(remaining):
            poly[remaining[i]] = 1
            poly[remaining[i + 1]] = -1
            i += 2
            made += 1

    pad(rem_even, pad_needed // 4 + 1)
    pad(rem_odd, pad_needed // 4 + 1)

    return poly


def generate_poly(
    N, q, target_even, target_odd, density, rng, need_invertible=True, max_tries=500
):
    for _ in range(max_tries):
        poly = constrained_ternary(N, target_even, target_odd, density, rng)
        se, so = sum_even_odd(poly, N)
        assert se == target_even and so == target_odd
        if not need_invertible:
            return poly
        try:
            invert_mod_q(poly, N, q)
            return poly
        except ValueError:
            continue
    raise RuntimeError(
        "failed to generate an invertible polynomial with the requested constraints"
    )


def weighted_trace(f, g, N, q_prime):
    fg = poly_mul_cyclic(f, g, N, q_prime)
    return sum((i + 1) * c for i, c in enumerate(fg)) % q_prime
