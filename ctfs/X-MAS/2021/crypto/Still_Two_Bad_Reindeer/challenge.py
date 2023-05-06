import struct
import numpy as np
from constants import *


def rotate_left(word, shift):
    return np.bitwise_or(np.left_shift(word, shift), np.right_shift(word, WORD_SIZE - shift))


def rotate_right(word, shift):
    return np.bitwise_or(np.right_shift(word, shift), np.left_shift(word, WORD_SIZE - shift))


def round_func(w_0, w_1, key_arr, index):
    word_0, word_1 = np.uint64(int(w_0)), np.uint64(int(w_1))

    word_0 += key_arr[0]
    word_1 += word_0
    word_1 = rotate_left(np.array([word_1], dtype=np.uint64), ROT_CONSTANTS[2 * index])[0]
    word_1 += key_arr[1]
    word_0 = rotate_right(np.array([word_0], dtype=np.uint64), ROT_CONSTANTS[2 * index + 1])[0]

    return np.array([word_0, word_1], dtype=np.uint64)


def encrypt(msg, key):
    for i in range(0, KEY_SIZE // BLOCK_SIZE, BLOCK_SIZE // WORD_SIZE):
        msg = round_func(msg[0], msg[1], key[i: i + BLOCK_SIZE // WORD_SIZE], i // (BLOCK_SIZE // WORD_SIZE))

    return msg


def pad(data, length):
    data_to_add = (length - len(data) % length) % length
    data += bytes(data_to_add)
    return data


def hash_func(salt, msg, key):
    key = np.frombuffer(key, dtype=np.uint64)
    data = np.frombuffer(pad(msg, BLOCK_SIZE // 8), dtype=np.uint64)

    state = np.frombuffer(salt, dtype=np.uint64)
    assert len(state) == BLOCK_SIZE // WORD_SIZE
    signature = b''

    for i in range(0, len(data)):
        state = np.array([state[0] + data[i], state[1]], dtype=np.uint64)
        state = encrypt(state, key)

    for i in range(BLOCK_SIZE // WORD_SIZE):
        signature += struct.pack('<Q', state[0])
        state = encrypt(state, key)

    return signature
