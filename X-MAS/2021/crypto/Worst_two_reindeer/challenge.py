from utils import *
from constants import *


def round_function(inp, key):
    i1 = inp[:HALF_WORD_SIZE]
    i0 = inp[HALF_WORD_SIZE:]
    k1 = key[:HALF_WORD_SIZE]
    k0 = key[HALF_WORD_SIZE:]

    x = 2 * k1[7] + k1[3]

    o1 = rotate_right(xor(i0, k0), x)
    o0 = xor(rotate_left(i1, 3), k1)

    return o1 + o0


class cipher:
    def __init__(self, key):
        assert len(key) == KEY_SIZE // 8
        self.key = bytes_2_bit_array(key)
        self.round_keys = self._get_key_schedule()

    def _get_key_schedule(self):
        key_copy = self.key
        keys = []

        for i in range(ROUNDS):
            k3 = key_copy[0: HALF_WORD_SIZE]
            k1 = key_copy[HALF_WORD_SIZE: 2 * HALF_WORD_SIZE]
            k2 = key_copy[2 * HALF_WORD_SIZE: 3 * HALF_WORD_SIZE]
            k0 = key_copy[-HALF_WORD_SIZE:]

            keys.append(k1 + k0)

            k0 = xor(rotate_left(k0, 7), k1)
            k2 = rotate_right(xor(k2, k3), 5)
            k3 = rotate_left(xor(k3, k1), 2)
            k1 = xor(rotate_right(k1, 6), k2)

            key_copy = k3 + k2 + k1 + k0

        return keys

    def encrypt(self, plaintext):
        pt = bytes_2_bit_array(plaintext)
        assert len(pt) == BLOCK_SIZE

        pt1 = pt[:WORD_SIZE]
        pt0 = pt[WORD_SIZE:]

        for i in range(ROUNDS):
            pt1, pt0 = pt0, xor(pt1, round_function(pt0, self.round_keys[i]))

        return bit_array_2_bytes(pt1 + pt0)

    def decrypt(self, ciphertext):
        ct = bytes_2_bit_array(ciphertext)
        assert len(ct) == BLOCK_SIZE

        ct0 = ct[:WORD_SIZE]
        ct1 = ct[WORD_SIZE:]

        for i in range(ROUNDS - 1, -1, -1):
            ct1, ct0 = ct0, xor(ct1, round_function(ct0, self.round_keys[i]))

        return bit_array_2_bytes(ct0 + ct1)
