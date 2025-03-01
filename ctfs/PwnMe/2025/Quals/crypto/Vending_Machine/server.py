#!/usr/bin/env python3
from tinyec.ec import SubGroup, Curve
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from json import loads, dumps
from hashlib import sha3_256
from random import choice
from os import urandom
from flag import FLAG
import secrets
import time

class SignatureManager:
    def __init__(self):
        # FRP256v1 Parameters
        self.p = 0xf1fd178c0b3ad58f10126de8ce42435b3961adbcabc8ca6de8fcf353d86e9c03
        self.a = 0xf1fd178c0b3ad58f10126de8ce42435b3961adbcabc8ca6de8fcf353d86e9c00
        self.b = 0xee353fca5428a9300d4aba754a44c00fdfec0c9ae4b1a1803075ed967b7bb73f
        self.Gx = 0xb6b3d4c356c139eb31183d4749d423958c27d2dcaf98b70164c97a2dd98f5cff
        self.Gy = 0x6142e0f7c8b204911f9271f0f3ecef8c2701c307e8e4c9e183115a1554062cfb
        self.n = 0xf1fd178c0b3ad58f10126de8ce42435b53dc67e140d2bf941ffdd459c6d655e1
        self.h = 1

        subgroup = SubGroup(self.p, (self.Gx, self.Gy), self.n, self.h)
        self.curve = Curve(self.a, self.b, subgroup, name="CustomCurve")

        self.P = self.curve.g
        self.d = int.from_bytes(urandom(32), "big")
        while self.d >= self.n:
            self.d = int.from_bytes(urandom(32), "big")
        self.Q = self.d * self.P
        self.salt = int.from_bytes(urandom(32), "big") % self.n

    def inverse(self, a, n):
        return pow(a, -1, n)

    def gen_sign(self, m: bytes, alea_1, alea_2):
        a = int(alea_1)
        b = int(alea_2)
        assert a**2 < b**2 < 2**120 - 1
        c = (hash(a) - hash(b)) * int.from_bytes(urandom(32), "big") ^ 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        randomized_main_part_l = 249
        randomized_part = ""
        for _ in range(256 - randomized_main_part_l):
            randomized_part += choice(bin(c).split("0b")[1])
        parity = int(randomized_part, 2) % 2
        randomized_part = bin(self.salt ^ int(randomized_part, 2))[-(256 - randomized_main_part_l):]
        k = 0xFF000000000000000000000000000000000000000000000000000000000000FF ^ int(randomized_part + bin(secrets.randbits(randomized_main_part_l)).split("0b")[1].zfill(randomized_main_part_l) if parity else bin(secrets.randbits(randomized_main_part_l)) + randomized_part, 2)
        e = int.from_bytes(sha3_256(m).digest(), "big")
        R = k * self.P
        r = R.x % self.n
        assert r != 0
        s = (self.inverse(k, self.n) * (e + self.d * r)) % self.n
        return r, s, int.from_bytes(m, "big")

    def verify(self, m: bytes, r: int, s: int):
        e = int.from_bytes(sha3_256(m).digest(), "big")
        assert 0 < r < self.n and 0 < s < self.n
        w = self.inverse(s, self.n)
        u1 = (e * w) % self.n
        u2 = (r * w) % self.n
        P_ = u1 * self.P + u2 * self.Q
        return r == P_.x % self.n


class Server:
    def __init__(self):
        self.signature_manager = SignatureManager()
        self.credits = 1
        self.signatures = []
        self.credit_currency = 0
        key = sha3_256(self.signature_manager.d.to_bytes(32, "big")).digest()[:16]
        self.iv = urandom(16)
        cipher = AES.new(key, IV=self.iv, mode=AES.MODE_CBC)
        self.encrypted_flag = cipher.encrypt(pad(FLAG.encode(), 16)).hex()
        self.used_credit = 0

    def show_credits(self):
        return {"credits": self.credits}

    def show_currency(self):
        return {"currency": self.credit_currency}

    def get_encrypted_flag(self):
        return {"encrypted_flag": self.encrypted_flag, "iv": self.iv.hex()}

    def get_new_signatures(self, alea_1, alea_2):
        if self.credits > 0:
            self.credits -= 1
            self.used_credit += 1
            new_signatures = []
            for i in range(10):
                m = sha3_256(b"this is my lovely loved distributed item " + str(i+10*self.used_credit).encode()).digest()
                r,s,_ = self.signature_manager.gen_sign(m, alea_1, alea_2)
                new_signatures.append((r, s))
                self.signatures.append((m.hex(), r, s))
            # ...Yeah, it's long, but it's just like vending machines... the cans take forever to drop, it's maddening...
            time.sleep(90)
            return {"signatures": new_signatures}
        else:
            return {"error": "Not enough credits."}

    def verify_proof_of_ownership(self, owner_proofs):
        owner_proofs = [tuple(item) for item in owner_proofs]
        if len(set(owner_proofs)) != self.credit_currency:
            return False
        for owner_proof in owner_proofs:
            if not self.signature_manager.verify(bytes.fromhex(owner_proof[0]), owner_proof[1], owner_proof[2]) or owner_proof in self.signatures:
                return False
        return True

    def buy_credit(self, owner_proofs):
        if self.verify_proof_of_ownership(owner_proofs):
            self.credits += 1
            # each credit cost more and more proofs to ensure you are the owner
            self.credit_currency += 5
            return {"status": "success", "credits": self.credits, "credit_currency": self.credit_currency}
        else:
            return {"error": f"You need {self.credit_currency} *NEW* signatures to buy more credits."}


def main():
    server = Server()
    print("Welcome to the signatures distributor, this is what you can do:")
    print("1. Show credits")
    print("2. Show currency")
    print("3. Get encrypted flag")
    print("4. Get signatures")
    print("5. Buy credit")
    print("6. Exit")
    
    while True:
        try:
            command = loads(input("Enter your command in JSON format: "))
            if "action" not in command:
                print({"error": "Invalid command format."})
                continue

            action = command["action"]

            if action == "show_credits":
                print(server.show_credits())

            elif action == "show_currency":
                print(server.show_currency())

            elif action == "get_encrypted_flag":
                print(server.get_encrypted_flag())

            elif action == "get_signatures":
                if "alea_1" not in command or "alea_2" not in command:
                    print({"error": "Invalid command format."})
                alea_1 = command["alea_1"]
                alea_2 = command["alea_2"]
                print(server.get_new_signatures(alea_1, alea_2))

            elif action == "buy_credit":
                if "owner_proofs" not in command:
                    print({"error": "Invalid command format."})
                print(server.buy_credit(command["owner_proofs"]))
            
            elif action == "exit":
                print({"status": "Goodbye!"})
                break
            
            else:
                print({"error": "Unknown action."})
        except Exception as e:
            print({"error": str(e)})

if __name__ == "__main__":
    main()
