Psst, I found a little something in the server files :O

```
def _is_probable_prime(candidate: int, rounds: int = 24) -> bool:
    if candidate < 2:
        return False
    for prime in _SMALL_PRIMES:
        if candidate == prime:
            return True
        if candidate % prime == 0:
            return False
    d = candidate - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(rounds):
        a = secrets.randbelow(candidate - 3) + 2
        x = pow(a, d, candidate)
        if x in (1, candidate - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, candidate)
            if x == candidate - 1:
                break
        else:
            return False
    return True


def _generate_prime(bits: int, exponent: int = 65537) -> int:
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if (candidate - 1) % exponent == 0:
            continue
        if _is_probable_prime(candidate):
            return candidate


def _generate_rsa_key() -> rsa.RSAPrivateKey:
    exponent = 65537
    # Keep the public modulus exactly 1024 bits
    while True:
        p = _generate_prime(512, exponent)
        if p * p >= (1 << 1023):
            break
    candidate = (p + (1 << 240)) | 1
    q = 0
    while candidate.bit_length() == 512:
        if (candidate - 1) % exponent and _is_probable_prime(candidate):
            q = candidate
            break
        candidate += 2
    if not q:
        return _generate_rsa_key()
    if p == q:
        return _generate_rsa_key()
    p, q = max(p, q), min(p, q)
    n = p * q
    lam = ((p - 1) * (q - 1)) // gcd(p - 1, q - 1)
    d = pow(exponent, -1, lam)
    public = rsa.RSAPublicNumbers(exponent, n)
    private = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=d % (p - 1),
        dmq1=d % (q - 1),
        iqmp=pow(q, -1, p),
        public_numbers=public,
    )
    return private.private_key()
```