"""
This is an (incomplete) implement for a new (and experimental) secret/password
sharing scheme.

The idea is simple. Basically, a secret or password is turned into a set of
finite field elements and each share is just a linear combination of these
elements. On the other hand, when enough shares are collected, the finite field
elements are determined, allowing the original secret or password to be
recovered.
"""
from typing import List
from secrets import randbelow
import string

ALLOWED_CHARS = string.ascii_lowercase + string.digits + "_"
P = len(ALLOWED_CHARS)
INT_TO_CHAR = {}
CHAR_TO_INT = {}
for _i, _c in enumerate(ALLOWED_CHARS):
    INT_TO_CHAR[_i] = _c
    CHAR_TO_INT[_c] = _i


def get_shares(password: str, n: int, t: int) -> List[str]:
    """
    Get password shares.

    Args:
        password: the password to be shared.
        n: the number of shares returned.
        t: the minimum number of shares needed to recover the password.

    Returns:
        the shares.
    """
    assert len(password) <= t
    assert n > 0

    ffes = [CHAR_TO_INT[c] for c in password]
    ffes += [randbelow(P) for _ in range(t - len(password))]
    result = []
    for _ in range(n):
        coeffs = [randbelow(P) for _ in range(len(ffes))]
        s = sum([x * y for x, y in zip(coeffs, ffes)]) % P
        coeffs.append(s)
        result.append("".join(INT_TO_CHAR[i] for i in coeffs))

    return result


def combine_shares(shares: List[str]) -> str:
    raise Exception("unimplemented")


def main():
    pw_len = 16
    password = "".join(INT_TO_CHAR[randbelow(P)] for _ in range(pw_len))

    # how about n < t :D
    n = 16
    t = 32

    for _ in range(2022):
        line = input()
        if line == password:
            from secret import FLAG
            print(FLAG)
            return
        else:
            print(get_shares(password, n, t))


if __name__ == '__main__':
    main()
