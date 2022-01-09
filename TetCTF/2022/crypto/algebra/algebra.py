# We will be working with Fp
p = 50824208494214622675210983238467313009841434758617398532295301998201478298245257311594403096942992643947506323356996857413985105233960391416730079425326309

# Just a random constant
C = 803799120267736039902689148809657862377959420031713529926996228010552678684828445053154435325462622566051992510975853540073683867248578880146673607388918

INFINITY = "INF"


# Here's the random operator I threw in.
def op(x1, x2):
    """Returns `(x1 + x2 + 2 * C * x1 * x2) / (1 - x1 * x2)`."""
    if x2 == INFINITY:
        x1, x2 = x2, x1
    if x1 == INFINITY:
        if x2 == INFINITY:
            return (-2 * C) % p
        elif x2 == 0:
            return INFINITY
        else:
            return -(1 + 2 * C * x2) * pow(x2, -1, p) % p
    if x1 * x2 == 1:
        return INFINITY
    return (x1 + x2 + 2 * C * x1 * x2) * pow(1 - x1 * x2, -1, p) % p


# Somehow, the associativity law holds.
assert op(op(2020, 2021), 2022) == op(2020, op(2021, 2022))


# The double-and-add algorithm for `op`
def repeated_op(x, k):
    """Returns `x op x op ... op x` (`x` appears `k` times)"""
    s = 0
    while k > 0:
        if k & 1:
            s = op(s, x)
        k = k >> 1
        x = op(x, x)
    return s


# Here's the most interesting thing:
assert repeated_op(2022, p - 1) == 0


# For this reason, I suspect there's a homomorphism `f` from this weird group
# (Fp with INFINITY under `op`) to <Fp, *>. If you can find one, I will give
# you the flag.
def main():
    from secrets import randbelow
    a, b = [randbelow(p) for _ in range(2)]
    m, n = [randbelow(p - 1) for _ in range(2)]
    c = op(repeated_op(a, m), repeated_op(b, n))
    print(a)
    print(b)
    print(c)

    # give me f(a), f(b), f(c)
    fa = int(input())
    fb = int(input())
    fc = int(input())
    if pow(fa, m, p) * pow(fb, n, p) % p == fc:
        from secret import FLAG
        print(FLAG[:pow(fc, 4, p)])


if __name__ == '__main__':
    main()
