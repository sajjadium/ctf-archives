#!/usr/bin/env python3
import os
import sys
import hashlib
import random

with open("flag.txt") as f:
    flag = f.read().strip()

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def inv_mod(x, m):
    return pow(x, -1, m)


def on_curve(x, y):
    return (y * y - x * x * x - A * x - B) % P == 0


def ec_add(P1, P2):
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if P1 == P2:
        lam = (3 * x1 * x1 + A) * inv_mod(2 * y1 % P, P) % P
    else:
        lam = (y2 - y1) * inv_mod((x2 - x1) % P, P) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)


def ec_mul(k, pt):
    if k % N == 0 or pt is None:
        return None
    k %= N
    R = None
    Q = pt
    while k:
        if k & 1:
            R = ec_add(R, Q)
        Q = ec_add(Q, Q)
        k >>= 1
    return R


def sha256i(msg):
    return int.from_bytes(hashlib.sha256(msg).digest(), "big")


A_HIGH_SIZE = 20
A_LOW_SIZE = 20
B_SIZE = 128
C_BYTES = (256 - B_SIZE) // 8
D_BYTES = (256 - A_HIGH_SIZE - A_LOW_SIZE) // 8
D_SIZE = 256 - A_HIGH_SIZE - A_LOW_SIZE
UNIT_COUNT = 5
SIGN_LIMIT = 4
TABLE_SIZE = 78
TABLE_LIMIT = 9
SKIP_COUNT = 622
MASK32 = (1 << 32) - 1
MASK64 = (1 << 64) - 1

BANNER = """
==================== PIYAKCRYPT ====================
[1] Show public records
[2] Show damaged record
[3] Request a signature
[4] Check side room
[5] Open data panel
[6] Submit code
[7] Exit
====================================================
"""


def parse_message(s):
    s = s.strip()
    if s.startswith("0x"):
        h = s[2:]
        if len(h) % 2:
            h = "0" + h
        return bytes.fromhex(h)
    return s.encode()


def rol32(x, r):
    r &= 31
    return ((x << r) | (x >> (32 - r))) & MASK32


def rol64(x, r):
    r &= 63
    return ((x << r) | (x >> (64 - r))) & MASK64


def panel_value(x, pos):
    salt = (0xA5A5A5A5 + pos * 0x6D2B79F5) & MASK32
    bump = (0x9E3779B9 ^ (pos * 0x85EBCA6B)) & MASK32
    y = rol32(x ^ salt, pos * 7 + 3)
    return (y + bump) & MASK32


def fold_piece(x, pos, lane):
    x ^= ((pos + 1) * 0xD6E8FEB86659FD93 + lane * 0xA0761D6478BD642F) & MASK64
    x = rol64(x, 17 + pos * 9 + lane * 23)
    x = (x * 0x9E6C63D0676A9A99 + 0xD1B54A32D192ED03) & MASK64
    return x


def make_piece(a, b, pos):
    return (fold_piece(a, pos, 0) << 64) | fold_piece(b, pos, 1)


def main():
    tag_high = random.getrandbits(A_HIGH_SIZE)
    tag_low = random.getrandbits(A_LOW_SIZE)
    _ = [random.getrandbits(32) for _ in range(SKIP_COUNT)]

    units = []
    for _ in range(UNIT_COUNT):
        piece = int.from_bytes(os.urandom(D_BYTES), "big")
        secret = ((tag_high << (D_SIZE + A_LOW_SIZE)) | (piece << A_LOW_SIZE) | tag_low) % N
        if secret == 0:
            secret = 1
        pub = ec_mul(secret, (Gx, Gy))
        assert pub and on_curve(*pub)
        units.append({"secret": secret, "pub": pub, "used": 0})
    table_reads = 0
    total_signatures = 0

    print(r"""
       _____ _             _     _____                  _
      |  __ (_)           | |   / ____|                | |
      | |__) | _   _  __ _| | _| |     _ __ _   _ _ __ | |_
      |  ___/| | | | |/ _` | |/ / |    | '__| | | | '_ \| __|
      | |    | | |_| | (_| |   <| |____| |  | |_| | |_) | |_
      |_|    |_|\__, |\__,_|_|\_\_____|_|   \__, | .__/ \__|
                 __/ |                        __/ | |
                |___/                        |___/|_|
    """)

    while True:
        print(BANNER)
        try:
            ch = int(input("  menu> ").strip())
        except Exception:
            ch = 0

        if ch == 1:
            print()
            print("  Public records:")
            print()
            for i, unit in enumerate(units):
                qx, qy = unit["pub"]
                print(f"    Unit #{i}:")
                print(f"      X = 0x{qx:064x}")
                print(f"      Y = 0x{qy:064x}")
                print()

        elif ch == 2:
            print()
            print("  Damaged record:")
            print()
            print(f"    record_high = 0x{tag_high:05x}")
            print(f"    record_low  = 0x{tag_low:05x}")
            print()

        elif ch == 3:
            if total_signatures >= UNIT_COUNT * SIGN_LIMIT:
                print()
                print("  No more signatures are available.")
                continue

            print()
            try:
                idx = int(input(f"  Choose unit (0-{UNIT_COUNT - 1}): ").strip())
            except Exception:
                print("  Invalid unit.")
                continue
            if idx < 0 or idx >= UNIT_COUNT:
                print("  Invalid unit.")
                continue
            if units[idx]["used"] >= SIGN_LIMIT:
                print(f"  Unit #{idx} is unavailable.")
                continue

            text = input("  Message (text or 0xHEX): ")
            msg = parse_message(text)
            z = sha256i(msg) % N
            secret = units[idx]["secret"]

            chunk_a = make_piece(
                random.getrandbits(64),
                random.getrandbits(64),
                total_signatures,
            )
            chunk_b = int.from_bytes(os.urandom(C_BYTES), "big")
            k = ((chunk_a << (256 - B_SIZE)) | chunk_b) % N
            while k == 0:
                chunk_a = make_piece(
                    random.getrandbits(64),
                    random.getrandbits(64),
                    total_signatures,
                )
                chunk_b = int.from_bytes(os.urandom(C_BYTES), "big")
                k = ((chunk_a << (256 - B_SIZE)) | chunk_b) % N

            R = ec_mul(k, (Gx, Gy))
            r = R[0] % N
            while r == 0:
                chunk_a = make_piece(
                    random.getrandbits(64),
                    random.getrandbits(64),
                    total_signatures,
                )
                chunk_b = int.from_bytes(os.urandom(C_BYTES), "big")
                k = ((chunk_a << (256 - B_SIZE)) | chunk_b) % N
                R = ec_mul(k, (Gx, Gy))
                r = R[0] % N

            s = (inv_mod(k, N) * (z + r * secret)) % N
            assert s != 0

            print()
            print(f"  Signature #{total_signatures} from unit #{idx}:")
            print()
            print(f"    z = {z}")
            print(f"    r = {r}")
            print(f"    s = {s}")
            print()

            units[idx]["used"] += 1
            total_signatures += 1

        elif ch == 4:
            print()
            print("  The side room is empty.")
            print()

        elif ch == 5:
            if table_reads >= TABLE_LIMIT:
                print()
                print("  The data panel is unavailable.")
                continue

            print()
            print("  Data panel:")
            print()
            for i in range(TABLE_SIZE):
                pos = table_reads * TABLE_SIZE + i
                v = random.getrandbits(32)
                print(f"    entry_{pos:03d} = 0x{panel_value(v, pos):08x}")
            print()

            table_reads += 1

        elif ch == 6:
            print()
            try:
                guess = int(input("  Code (integer): ").strip(), 0)
            except Exception:
                print("  Invalid code.")
                continue

            for i, unit in enumerate(units):
                if guess == unit["secret"]:
                    print()
                    print(f"  Accepted for unit #{i}.")
                    print()
                    print(f"  {flag}", flush=True)
                    sys.exit(0)

            print()
            print("  Rejected.", flush=True)
            sys.exit(0)

        elif ch == 7:
            print()
            print("  Goodbye.")
            return

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
