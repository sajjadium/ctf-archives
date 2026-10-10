#!/usr/bin/python3

import random


def encrypt(m_bytes):
    l = len(m_bytes)
    pad = random.getrandbits(l * 8).to_bytes(l, 'big')
    return bytes([a ^ b for (a, b) in zip(m_bytes, pad)]).hex()


def main():
    flag = open("flag.txt", "rb").read()
    assert(flag.startswith(b"Blockhouse{") and flag.endswith(b"}"))
    [print(encrypt(flag)) for _ in range(300)]


if __name__ == '__main__':
    main()
