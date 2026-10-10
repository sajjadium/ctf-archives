#!/usr/bin/python3

import base64
import binascii
import hashlib
import json
import signal
import sys

from sage.all import *
from Crypto.Util.number import *

BANNER = """
    ███      ▄█   ▄████████    ▄█   ▄█▄    ▄████████     ███             ▄████████    ▄█    █▄     ▄██████▄     ▄███████▄
▀█████████▄ ███  ███    ███   ███ ▄███▀   ███    ███ ▀█████████▄        ███    ███   ███    ███   ███    ███   ███    ███
   ▀███▀▀██ ███▌ ███    █▀    ███▐██▀     ███    █▀     ▀███▀▀██        ███    █▀    ███    ███   ███    ███   ███    ███
    ███   ▀ ███▌ ███         ▄█████▀     ▄███▄▄▄         ███   ▀        ███         ▄███▄▄▄▄███▄▄ ███    ███   ███    ███
    ███     ███▌ ███        ▀▀█████▄    ▀▀███▀▀▀         ███          ▀███████████ ▀▀███▀▀▀▀███▀  ███    ███ ▀█████████▀
    ███     ███  ███    █▄    ███▐██▄     ███    █▄      ███                   ███   ███    ███   ███    ███   ███
    ███     ███  ███    ███   ███ ▀███▄   ███    ███     ███             ▄█    ███   ███    ███   ███    ███   ███
   ▄████▀   █▀   ████████▀    ███   ▀█▀   ██████████    ▄████▀         ▄████████▀    ███    █▀     ▀██████▀   ▄████▀
                              ▀

        In our shop, you are guaranteed to win!
"""

MENU = """
Choose an action:
    1) Get a free ticket
    2) Claim your prize
"""

class RNG:
    def __init__(self, p):
        assert isPrime(p), "p must be prime"
        self.p = Integer(p)
        self.F = GF(self.p)
        self.H = QuaternionAlgebra(self.F, -1, -1)

        self.i = self.H.gen(0)
        self.j = self.H.gen(1)
        self.k = self.i * self.j

        self.half = self.F(1) / self.F(2)

        while True:
            a = self.F.random_element()
            b = self.F.random_element()
            c = self.F.random_element()
            d = self.F.random_element()
            if b != 0:
                break

        self.q = a + b*self.i + c*self.j + d*self.k
        self.n = Integer(0)

    def seed(self):
        self.n = ZZ.random_element(self.p)

    def print_params(self):
        print(f"seed = {self.n}")
        print(f"q = {self.q}")

    def gen(self):
        Q = self.q ** int(self.n)
        ret = -self.half * (self.i * Q).reduced_trace()
        self.n += 1
        return int(ret)

class Signer:
    _p  = Integer(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
    _a4 = Integer(0)
    _a6 = Integer(7)
    _n  = Integer(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
    _Gx = Integer(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798)
    _Gy = Integer(0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

    def __init__(self, rng):
        self.rng = rng

        F = GF(self._p)
        self.E = EllipticCurve(F, [0, 0, 0, self._a4, self._a6])
        self.G = self.E(self._Gx, self._Gy)
        self.n = self._n

        self.d = Integer(1 + ZZ.random_element(self.n - 1))
        self.Q = (self.d * self.G)

        self.rng.seed()

    def _hash_to_int(self, msg):
        h = hashlib.sha256(msg).digest()
        return Integer(int.from_bytes(h, 'big')) % self.n

    def _next_k(self):
        while True:
            k = Integer(self.rng.gen())
            if k != 0:
                return k

    def sign(self, msg):
        z = self._hash_to_int(msg)

        while True:
            k = self._next_k()
            R = (k * self.G)
            if R.is_zero():
                continue
            r = Integer(R.xy()[0]) % self.n
            if r == 0:
                continue
            try:
                kinv = Integer(k).inverse_mod(self.n)
            except ZeroDivisionError:
                continue
            s = (kinv * (z + r * self.d)) % self.n
            if s == 0:
                continue
            return (int(r), int(s))

    def verify(self, msg, sig):
        r, s = map(Integer, sig)
        if not (1 <= r < self.n and 1 <= s < self.n):
            return False

        z = self._hash_to_int(msg)
        try:
            w = Integer(s).inverse_mod(self.n)
        except ZeroDivisionError:
            return False
        u1 = (z * w) % self.n
        u2 = (r * w) % self.n
        V = u1 * self.G + u2 * self.Q
        if V.is_zero():
            return False
        xV = Integer(V.xy()[0]) % self.n
        return xV == r

    def pubkey(self):
        P = self.Q.xy()
        return (int(P[0]), int(P[1]))

    def privkey(self):
        return int(self.d)


class Ticket:
    def __init__(self, rng, signer, cnt = 1):
        self.signer = signer
        self.cnt = cnt
        self.rng = rng
        rng.seed()

    def reset(self):
        self.cnt = 1

    def fresh(self):
        if self.cnt <= 0:
            return "No more tickets for you..."
        self.cnt -= 1

        ticket_id = int(self.rng.gen())

        payload = {"ticket_id": ticket_id}
        payload_bytes = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode()

        r, s = self.signer.sign(payload_bytes)
        r_bytes = int(r).to_bytes(32, 'big')
        s_bytes = int(s).to_bytes(32, 'big')
        sig_hex = (r_bytes + s_bytes).hex()

        ticket = {
            "payload": payload,
            "signature": sig_hex,
        }

        ticket_json = json.dumps(ticket, separators=(',', ':'), sort_keys=True).encode()
        return base64.b64encode(ticket_json).decode()


class PrizePool:
    def __init__(self, signer, ticket_shop):
        self.signer = signer
        self.ticket_shop = ticket_shop
        self._used = set()


    def claim_prize(self, ticket_b64):
        try:
            raw = base64.b64decode(ticket_b64, validate=True)
        except Exception:
            return "Invalid ticket: bad base64"

        try:
            ticket = json.loads(raw.decode())
        except Exception:
            return "Invalid ticket: bad JSON"

        if not isinstance(ticket, dict) or "payload" not in ticket or "signature" not in ticket:
            return "Invalid ticket: missing fields"

        payload = ticket["payload"]
        sig_hex = ticket["signature"]

        if not isinstance(payload, dict) or "ticket_id" not in payload:
            return "Invalid ticket: bad payload"

        tid = payload["ticket_id"]
        try:
            tid = int(tid)
        except Exception:
            return "Invalid ticket: ticket_id not integer"

        payload_bytes = json.dumps({"ticket_id": tid}, separators=(',', ':'), sort_keys=True).encode()

        if not isinstance(sig_hex, str):
            return "Invalid ticket: signature not a string"
        try:
            sig_bytes = bytes.fromhex(sig_hex)
        except (ValueError, binascii.Error):
            return "Invalid ticket: signature not hex"

        if len(sig_bytes) != 64:
            return "Invalid ticket: signature wrong length"

        r = int.from_bytes(sig_bytes[:32], 'big')
        s = int.from_bytes(sig_bytes[32:], 'big')

        if not self.signer.verify(payload_bytes, (r, s)):
            return "Invalid ticket: bad signature"

        if tid in self._used:
            print("Go away hacker!")
            exit(1)

        self._used.add(tid)

        if tid == bytes_to_long(hashlib.sha256(b"I'd like the flag please").digest()):
            flag = open("flag.txt", "r").read()
            flag_prize = f"""
       ░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░▒▓█▓▒░
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░
       ░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░       ░▒▓██████▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░

                    {flag}
            """

            return flag_prize

        if tid % 2 == 0:
            self.ticket_shop.reset()
            ticket = self.ticket_shop.fresh()
            return f"You won a brand new ticket: {ticket}"

        prize = """You won some free candy:

                     /\.--./\\
                     \/'--'\/

             /\.--./\        /\.--./\\
             \/'--'\/        \/'--'\/
        """

        return prize



def timeout_handler(signum, frame):
    print("Timeout!")
    sys.exit(1)


def main():
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(120)

    print(BANNER)

    rng_ticket = RNG(int(Signer._n))
    rng_signer = copy(rng_ticket)

    signer = Signer(rng_signer)

    ticket_shop = Ticket(rng_ticket, signer)
    prize_pool = PrizePool(signer, ticket_shop);

    while True:
        print(MENU)
        option = int(input())
        if option not in [1, 2]:
            print("W00t?")
            continue

        if option == 1:
            print(f"{ticket_shop.fresh()}")
        else:
            print("Enter your ticket: ")
            ticket = input().strip()
            print(f"{prize_pool.claim_prize(ticket)}")



if __name__ == '__main__':
    main()
