#!/usr/bin/env python3
from __future__ import annotations

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import random
import struct

BLOCK_SIZE = 16
INDEX_SIZE = 20
KEY_SIZE = 16

LOCAL_NONCE = bytes(range(BLOCK_SIZE))


def random_index() -> list[int]:
    return [random.randint(0, 64) for _ in range(INDEX_SIZE)]


def index_to_bytes(index: list[int]) -> bytes:
    assert len(index) == INDEX_SIZE
    return struct.pack(f"<{INDEX_SIZE}b", *index)


def index_from_bytes(index_bytes: bytes) -> list[int]:
    assert len(index_bytes) == INDEX_SIZE
    return list(struct.unpack(f"<{INDEX_SIZE}b", index_bytes))


class GF:
    MOD = 0x19F2BBF3EF3A2AB6684710EB139F3A9AD

    def __init__(self, v: int):
        assert 0 <= v < 2**128
        self.v = v

    @classmethod
    def _double(cls, v):
        if v >> 127:
            new_v = (v << 1) ^ cls.MOD
        else:
            new_v = v << 1
        return new_v

    def __add__(self, other):
        return GF(self.v ^ other.v)

    def __iadd__(self, other):
        self.v ^= other.v
        return self

    def __mul__(self, other):
        res, cur = 0, self.v
        for i in range(128):
            if (other.v >> i) & 1:
                res ^= cur
            cur = self._double(cur)
        return GF(res)

    def __imul__(self, other):
        res = self * other
        self.v = res.v
        return self

    def __pow__(self, y):
        y %= 2**128 - 1
        res, cur = GF(1), GF(self.v)
        while y:
            if y & 1:
                res *= cur
            cur *= cur
            y >>= 1
        return res

    @classmethod
    def from_bytes(cls, b: bytes):
        assert len(b) <= BLOCK_SIZE
        return cls(int.from_bytes(b, "little"))

    def to_bytes(self) -> bytes:
        return self.v.to_bytes(BLOCK_SIZE, "little")


class FileCipher:
    def __init__(self):
        with open("key", "rb") as f:
            key = f.read(KEY_SIZE)
            assert len(key) == KEY_SIZE

        self.cipher = AES.new(key, AES.MODE_ECB)

        with open("vectors", "rb") as f:
            self.vectors = []
            for _ in range(INDEX_SIZE):
                vec = f.read(BLOCK_SIZE)
                assert len(vec) == BLOCK_SIZE
                self.vectors.append(GF.from_bytes(vec))

    def encrypt(self, nonce: bytes, index: list[int], plaintext: bytes) -> bytes:
        data = pad(plaintext, BLOCK_SIZE)

        assert len(data) % BLOCK_SIZE == 0
        assert len(nonce) == BLOCK_SIZE
        assert len(index) == INDEX_SIZE

        return self._do_crypto(nonce, index, data, is_decrypt=False)

    def decrypt(self, nonce: bytes, index: list[int], ciphertext: bytes) -> bytes:
        assert len(ciphertext) % BLOCK_SIZE == 0
        assert len(nonce) == BLOCK_SIZE
        assert len(index) == INDEX_SIZE

        return self._do_crypto(nonce, index, ciphertext, is_decrypt=True)

    def _initialize_alpha(self, nonce: bytes, index: list[int]) -> GF:
        encrypted_nonce = self.cipher.encrypt(nonce)
        alpha = GF.from_bytes(encrypted_nonce)

        for vector, exponent in zip(self.vectors, index):
            alpha *= vector**exponent

        return alpha

    def _update_alpha(self, index: list[int], alpha: GF, block_num: int) -> GF:
        block_num %= INDEX_SIZE
        index[block_num] += 1
        return alpha * self.vectors[block_num]

    def _gf_encrypt(self, v: GF) -> GF:
        enc = self.cipher.encrypt(v.to_bytes())
        return GF.from_bytes(enc)

    def _gf_decrypt(self, v: GF) -> GF:
        dec = self.cipher.decrypt(v.to_bytes())
        return GF.from_bytes(dec)

    def _do_crypto(
        self, nonce: bytes, index: list[int], data: bytes, is_decrypt: bool = False
    ) -> bytes:
        index = index[:]  # Copy index

        # 1. Initialize alpha
        alpha = self._initialize_alpha(nonce, index)

        result = b""
        for offset in range(0, len(data), BLOCK_SIZE):
            if index == [0] * INDEX_SIZE:
                print("Index cannot be NULL")
                return b""
            block = data[offset : offset + BLOCK_SIZE]
            b = GF.from_bytes(block)

            # 2. Do enc/dec
            b += alpha
            if is_decrypt:
                b = self._gf_decrypt(b)
            else:
                b = self._gf_encrypt(b)
            b += alpha
            result += b.to_bytes()

            # 3. Update alpha
            alpha = self._update_alpha(index, alpha, offset // BLOCK_SIZE)

        return result
