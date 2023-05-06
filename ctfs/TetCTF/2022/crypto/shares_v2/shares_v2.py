"""
In this new version, I introduce a new feature: master share. A master share
is always required to recover the original secret/password.

I implement this feature by using the master share to "encrypt" the linear
combination results.
"""
from shares import *
from typing import Tuple, List
from secrets import randbits, randbelow

MASTER_SHARE_SZ = 128


def get_shares_v2(password: str, n: int, t: int) -> Tuple[int, List[str]]:
    """
    Get password shares.

    Args:
        password: the password to be shared.
        n: the number of non-master shares returned.
        t: the minimum number of non-master shares needed to recover the
           password.

    Returns:
        the shares, including the master share (n + 1 shares in total).
    """
    assert n <= MASTER_SHARE_SZ
    master_share = randbits(MASTER_SHARE_SZ)
    unprocessed_non_master_shares = get_shares(password, n, t)
    non_master_shares = []
    for i, share in enumerate(unprocessed_non_master_shares):
        v = CHAR_TO_INT[share[-1]]
        if (master_share >> i) & 1:
            v = (v + P // 2) % P
        non_master_shares.append(share[:-1] + INT_TO_CHAR[v])

    return master_share, non_master_shares


def combine_shares_v2(master_share: int, non_master_shares: List[str]) -> str:
    raise Exception("unimplemented")


def main():
    pw_len = n = t = 32
    password = "".join(INT_TO_CHAR[randbelow(P)] for _ in range(pw_len))

    for _ in range(2022):
        line = input()
        if line == password:
            from secret import FLAG
            print(FLAG)
            return
        else:
            _, non_master_shares = get_shares_v2(password, n, t)
            print(non_master_shares)


if __name__ == '__main__':
    main()
