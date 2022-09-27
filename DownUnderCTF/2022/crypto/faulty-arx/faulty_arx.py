#!/usr/bin/env python3

import os
import signal
import random


FLAG = open(os.path.join(os.path.dirname(__file__), 'flag.txt'), 'r').read().strip()


def rol(x, d):
    return ((x << d) | (x >> (32 - d))) & 0xffffffff

def bytes_to_words(B):
    return [int.from_bytes(B[i:i+4], 'little') for i in range(0, len(B), 4)]

def words_to_bytes(W):
    return b''.join([w.to_bytes(4, 'little') for w in W])

class faulty_arx:
    def __init__(self, key, nonce):
        self.ROUNDS = 20
        self.counter = 0
        self.f = 0
        self.key = key
        self.nonce = nonce

    def _init_state(self, key, nonce, counter):
        state = bytes_to_words(b'downunderctf2022')
        state += bytes_to_words(key)
        state += [counter] + bytes_to_words(nonce)
        return state

    def _QR(self, S, a, b, c, d):
        S[a] = (S[a] + S[b]) & 0xffffffff; S[d] ^= S[a]; S[d] = rol(S[d], 16)
        S[c] = (S[c] + S[d]) & 0xffffffff; S[b] ^= S[c]; S[b] = rol(S[b], 12 ^ self.f)
        S[a] = (S[a] + S[b]) & 0xffffffff; S[d] ^= S[a]; S[d] = rol(S[d], 8)
        S[c] = (S[c] + S[d]) & 0xffffffff; S[b] ^= S[c]; S[b] = rol(S[b], 7)

    def block(self):
        initial_state = self._init_state(self.key, self.nonce, self.counter)
        state = initial_state.copy()
        for r in range(0, self.ROUNDS, 2):
            self._QR(state, 0, 4, 8, 12)
            self._QR(state, 1, 5, 9, 13)
            self._QR(state, 2, 6, 10, 14)
            self._QR(state, 3, 7, 11, 15)

            x = 0
            if r == self.ROUNDS - 2:
                x = random.randint(0, 4)

            if x == 1:
                self.f = 1
            self._QR(state, 0, 5, 10, 15)
            self.f = 0

            if x == 2:
                self.f = 1
            self._QR(state, 1, 6, 11, 12)
            self.f = 0

            if x == 3:
                self.f = 1
            self._QR(state, 2, 7, 8, 13)
            self.f = 0

            if x == 4:
                self.f = 1
            self._QR(state, 3, 4, 9, 14)
            self.f = 0

        out = [(i + s) & 0xffffffff for i, s in zip(initial_state, state)]
        self.counter += 1
        return words_to_bytes(out)

    def stream(self, length):
        out = bytearray()
        while length > 0:
            block = self.block()
            t = min(length, len(block))
            out += block[:t]
            length -= t
        return out


def main():
    key = os.urandom(16).hex().encode()
    nonce = os.urandom(12)
    print(nonce.hex())
    out = set()
    for _ in range(20):
        cipher = faulty_arx(key, nonce)
        out.add(cipher.stream(64).hex())
    for c in out:
        print(c)
    key_guess = input('key> ')
    if key_guess == key.decode():
        print(FLAG)
    else:
        print('Incorrect key!')


if __name__ == '__main__':
    signal.alarm(180)
    main()
