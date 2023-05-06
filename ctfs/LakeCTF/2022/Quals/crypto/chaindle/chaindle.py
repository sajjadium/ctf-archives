#!/usr/local/bin/python

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Random.random import shuffle

from enum import Enum
from hashlib import sha256
import json
import string


class Color(Enum):
    BLACK = "⬛"
    YELLOW = "🟨"
    GREEN = "🟩"

    def __str__(self):
        return str(self.value)


def get_color(answer: bytes, guess: bytes) -> list[Color]:
    assert len(answer) == len(guess), (
        f"Wrong guess length, " f"answer_len={len(answer)}, guess_len={len(guess)}"
    )

    n = len(answer)
    matched = [False] * n
    color = [Color.BLACK] * n

    for i in range(n):
        if answer[i] == guess[i]:
            matched[i] = True
            color[i] = Color.GREEN

    for i in range(n):
        if color[i] == Color.GREEN:
            continue
        for j in range(n):
            if matched[j] or answer[j] != guess[i]:
                continue
            matched[j] = True
            color[i] = Color.YELLOW

    return color


class Chaindle:
    def __init__(self, answer: bytes):
        self.answer = answer
        self.key = get_random_bytes(32)

    def guess(self, iv: bytes, ciphertext: bytes) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        return "".join(c.value for c in get_color(self.answer, plaintext))


def challenge() -> None:
    with open("flag.txt", "r") as f:
        FLAG = f.read().encode()

    answer = list(string.ascii_letters + string.digits + "+/")
    shuffle(answer)
    answer = "".join(answer).encode()
    ALL_GREEN = Color.GREEN.value * len(answer)

    chaindle = Chaindle(answer)
    for _ in range(256):
        guess = json.loads(input())
        result = chaindle.guess(
            bytes.fromhex(guess["iv"]),
            bytes.fromhex(guess["ciphertext"]),
        )
        print(json.dumps({"result": result}))
        if result == ALL_GREEN:
            print("Congrats!")
            break
    else:
        key = sha256(answer).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        FLAG = cipher.encrypt(pad(FLAG, 16))

    print(FLAG)


if __name__ == "__main__":
    challenge()
