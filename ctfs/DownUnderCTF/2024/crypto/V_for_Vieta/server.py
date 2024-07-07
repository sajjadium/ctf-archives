#!/usr/bin/env python3

import os
import random
import json
from enum import Enum


FLAG = os.getenv("FLAG", "DUCTF{dummy_flag}")


class State(Enum):
    INITIAL = 1
    TEST = 2
    QUIT = 3


class Server:
    def __init__(self):
        self.level = 2048
        self.target = 2048
        self.finish = 8
        self.state = State.INITIAL

    def win(self):
        return {
            "flag": FLAG,
        }

    def generate_k(self):
        self.k = random.getrandbits(self.level) ** 2
        self.state = State.TEST
        return {
            "k": self.k,
            "level": self.level,
        }

    def test(self, challenge):
        a, b = challenge["a"], challenge["b"]
        if a <= 0 or b <= 0:
            self.state = State.QUIT
            return {"error": "Your answer must be positive!"}

        if a.bit_length() <= self.target or b.bit_length() <= self.target:
            self.state = State.QUIT
            return {"error": "Your answer is too small!"}

        num = a**2 + a * b + b**2
        denom = 2 * a * b + 1

        if num % denom != 0 or num // denom != self.k:
            self.state = State.QUIT
            return {"error": "Your answer wasn't a solution!"}

        self.level -= self.level // 5

        if self.level <= self.finish:
            self.state = State.QUIT
            return self.win()
        else:
            return self.generate_k()


def main():
    server = Server()
    print("V equals negative V plus or minus the squareroot of V squared minus 4 V V all divided by 2 V!")

    while True:
        if server.state == State.INITIAL:
            print(json.dumps(server.generate_k()))
        elif server.state == State.TEST:
            challenge = json.loads(input())
            print(json.dumps(server.test(challenge)))
        elif server.state == State.QUIT:
            exit(0)


if __name__ == "__main__":
    main()
