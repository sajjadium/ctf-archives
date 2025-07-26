from hashlib import shake_256
import os
from typing import Callable


def xor(a, b):
    assert len(a) == len(b)
    return bytes([x ^ y for x, y in zip(a, b)])

def rotr(a, n):
    a = int.from_bytes(a, "big")
    a = ((a >> n) | (a << (32 - n))) & 0xFFFFFFFF
    a = a.to_bytes(4, "big")
    return a

ROTATION_SCHEDULE = [16, 16, 8, 8, 16, 16, 24, 24]

class Khufu:
    def __init__(self, key: bytes, n_rounds: int = 16):
        # modification using 16 byte key
        assert len(key) == 16
        self.auxkeys = [key[:8], key[8:]]

        assert n_rounds % 8 == 0
        self.n_rounds = n_rounds
        self.n_octets = self.n_rounds // 8
        self.sboxes = self._generate_sboxes(key)

    def _generate_sboxes(self, key: bytes) -> "list[list[bytes]]":
        material = shake_256(key).digest(256 * 4 * self.n_octets)
        material_index = 0

        def next_material() -> int:
            nonlocal material_index
            material_index += 1
            return material[material_index - 1]

        return [Khufu._generate_sbox(next_material) for _ in range(self.n_octets)]

    @staticmethod
    def _generate_sbox(next_material: Callable[[], int]) -> "list[bytes]":
        sbox = [bytearray([i] * 4) for i in range(256)]
        for col in range(4):
            for i in range(256 - 1):
                j = i + next_material() % (256 - i)
                sbox[i][col], sbox[j][col] = sbox[j][col], sbox[i][col]
        sbox = [bytes(b) for b in sbox]

        return sbox

    def encrypt_block(self, block: bytes) -> bytes:
        assert len(block) == 8
        block = xor(block, self.auxkeys[0])
        left, right = block[:4], block[4:]

        for octet in range(self.n_octets):
            sbox = self.sboxes[octet]
            for i in range(8):
                left = xor(left, sbox[right[-1]])
                right = rotr(right, ROTATION_SCHEDULE[i])
                left, right = right, left

        return xor(left + right, self.auxkeys[1])

    def encrypt(self, pt: bytes) -> bytes:
        padding = 8 - (len(pt) % 8)
        pt += bytes([padding] * padding)

        ct = bytearray()
        for i in range(0, len(pt), 8):
            block = pt[i : i + 8]
            ct.extend(self.encrypt_block(block))
        ct = bytes(ct)

        return ct

if __name__ == "__main__":
    khufu = Khufu(
        os.urandom(16),
        # I'll go easy on you this time
        n_rounds=8
    )

    encrypted_flag = khufu.encrypt(b"wwf{REDACTEDREDACTEDREDACTEDREDACTEDRED}")
    print("Flag:", encrypted_flag.hex())

    for _ in range(123):
        pt = bytes.fromhex(input("Try my encryption > "))
        ct = khufu.encrypt(pt)
        print("Result:", ct.hex())

    print("Enough already.")
