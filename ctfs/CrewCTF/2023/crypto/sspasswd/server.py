from Crypto.Util.number import *

# secret import
from param_secret import p, pollst
from ss_config import FLAG, ALICE_PW, BOB_PW


PWCHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@_'


assert len(ALICE_PW) == 12
assert len(BOB_PW) == 12
assert all([ch in PWCHARSET for ch in ALICE_PW])
assert all([ch in PWCHARSET for ch in BOB_PW])
assert len(FLAG) <= 64

ALICE_PW = ALICE_PW.encode()
BOB_PW = BOB_PW.encode()


def evalpoly(pollst, p, pnt):
    return sum([coef * pow(pnt, idx, p) for idx, coef in enumerate(pollst)]) % p


def main():
    assert evalpoly(pollst, p, 0) == int.from_bytes(FLAG, 'big')
    assert evalpoly(pollst, p, 1) == int.from_bytes(ALICE_PW, 'big')
    assert evalpoly(pollst, p, 2) == int.from_bytes(BOB_PW, 'big')
    assert len(pollst) == 4 + 1

    public_shares = []
    for pnt in [1337, 0xbeef, 0xcafe, 0xdead]:
        public_shares.append((pnt, evalpoly(pollst, p, pnt)))

    print(f"p = {p}")
    print(f"public_shares = {public_shares}")


if __name__ == '__main__':
    main()
