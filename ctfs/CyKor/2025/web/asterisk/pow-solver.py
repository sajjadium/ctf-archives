from __future__ import annotations

import base64
import hashlib
import json
import os
import threading
import time
from typing import Optional

# Paste the /pow/start token here.
CHALLENGE = ""

THREADS = os.cpu_count() or 1


def b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def leading_zero_bits(digest: bytes) -> int:
    total = 0
    for b in digest:
        if b == 0:
            total += 8
        else:
            total += 8 - b.bit_length()
            break
    return total


def parse_challenge(token: str):
    try:
        msg_b64, _sig = token.split(".")
        payload = json.loads(b64url_decode(msg_b64))
        bits = int(payload["bits"])
        salt = b64url_decode(payload["salt"])
        exp = int(payload["exp"])
    except Exception as e:  # noqa: BLE001
        raise ValueError("Invalid challenge token") from e

    if time.time() > exp:
        raise ValueError("Challenge already expired")
    return bits, salt, exp


def solve(bits: int, salt: bytes, threads: int) -> str:
    """
    Brute-force search for a suffix that satisfies the leading zero bits check.
    Uses simple str(counter) as the suffix to keep things deterministic.
    """
    stop = threading.Event()
    result: list[Optional[str]] = [None]

    def worker(start: int, step: int):
        counter = start
        while not stop.is_set():
            suffix = str(counter)
            h = hashlib.sha256(salt + suffix.encode()).digest()
            if leading_zero_bits(h) >= bits:
                result[0] = suffix
                stop.set()
                return
            counter += step

    threads = max(1, threads)
    pool = [threading.Thread(target=worker, args=(i, threads), daemon=True) for i in range(threads)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()

    if not result[0]:
        raise RuntimeError("Failed to find solution")
    return result[0]


def main():
    if not CHALLENGE:
        raise SystemExit("Please set the CHALLENGE constant to your token.")

    bits, salt, exp = parse_challenge(CHALLENGE)
    print(f"[+] Challenge parsed: bits={bits}, expires_in={int(exp - time.time())}s")
    print(f"[+] Salt length: {len(salt)} bytes")
    print(f"[+] Searching with {THREADS} threads ...")

    started = time.time()
    suffix = solve(bits, salt, THREADS)
    elapsed = time.time() - started
    print(f"[+] Found suffix: {suffix}")
    print(f"[+] Time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
