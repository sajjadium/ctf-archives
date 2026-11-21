#!/usr/bin/env python3
# Snake Charmer v3.1 - License Validator
# Validate your Outback Overflow ticket

import sys as _s, random as _r, hashlib as _h

_ = lambda _a: [_b ^ (_c % 7) for _c, _b in enumerate(_a)]
__ = lambda _a: (lambda _p, _d: [_d.__setitem__(_p[_i], _a[_i]) or None for _i in range(len(_a))] and _d)(
    (lambda _r2: (_r2.shuffle(_l := list(range(len(_a)))), _l)[1])(_r.Random(31337)),
    [0] * len(_a)
)
___ = lambda _a: (lambda: (
    _acc := [0],
    _res := [],
    [(_acc.__setitem__(0, (_acc[0] + _v) % 256), _res.append(_acc[0])) for _v in _a],
    _res
))()[-1]

# Expected output after transformation pipeline
_X = [94, 147, 244, 81, 130, 179, 38, 150, 15, 129, 242, 34, 141, 0, 51, 160, 7, 86, 205, 63, 114, 235, 86, 141, 247, 69]

def _verify(_input):
    if len(_input) != len(_X):
        return False
    _t1 = _([ord(_c) for _c in _input])
    _t2 = __(_t1)
    _t3 = ___(_t2)
    return _t3 == _X

def main():
    print("=" * 50)
    print("  Snake Charmer v3.1 - Ticket Validator")
    print("=" * 50)
    print()

    if len(_s.argv) > 1:
        ticket = _s.argv[1]
    else:
        ticket = input("Enter your ticket code: ")

    if _verify(ticket):
        print()
        print("[+] Valid ticket! Welcome to Outback Overflow!")
        print(f"[+] Your flag is: {ticket}")
    else:
        print()
        print("[-] Invalid ticket. Nice try, snake.")
        _s.exit(1)

if __name__ == "__main__":
    main()
