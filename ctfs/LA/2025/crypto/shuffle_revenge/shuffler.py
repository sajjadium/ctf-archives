#!/usr/local/bin/python3

from secrets import randbits
import os
import sys
import binascii


class LCG:

    def __init__(self, a: int, c: int, m: int, seed: int):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state


def shuffle_msg(msg: bytes, L: LCG) -> str:

    l = len(msg)

    positions = [L.next() for i in range(l)]

    sorted_msg = sorted(zip(positions, msg))

    output = bytes([c[1] for c in sorted_msg])

    return binascii.hexlify(output).decode()


secret = os.urandom(64)
length = len(secret)
assert length == 64

while True:
    a = randbits(64)
    c = randbits(64)
    m = 1 << 64
    seed = randbits(64)
    initial_iters = randbits(16)
    # https://en.wikipedia.org/wiki/Linear_congruential_generator#m_a_power_of_2,_c_%E2%89%A0_0
    if (c != 0 and c % 2 == 1) and (a % 4 == 1):
        print(f"LCG coefficients:\na={a}\nc={c}\nm={m}")
        break

L = LCG(a, c, m, seed)
for i in range(initial_iters):
    L.next()

shuffled_secret = shuffle_msg(secret, L)

while True:
    choice = input(
        "What do you want to do?\n1: Shuffle a message.\n2: Get the shuffled secret.\n3: Send the secret\n4: Quit.\n> "
    )
    if choice == "1":
        try:
            message = binascii.unhexlify(
                input("Ok. What do you have to say (hex)?\n").encode()
            )
            if len(message) > 256:
                print(f"I ain't reading allat.")
            else:
                print(f"Here you go: {shuffle_msg(message,L)}\n")
        except:
            print("Bad message!")
    elif choice == "2":
        print(f"Here you go: {shuffled_secret}\n")
    elif choice == "3":
        try:
            guess_secret = binascii.unhexlify(
                input("Send the secret in hex\n> ").encode()
            )
            if guess_secret == secret:
                print("Here's your flag:")
                print(open("secret_message.txt", "r").read())
            else:
                print("Wrong.")
        except:
            print("Bad secret!")
        sys.exit(0)
    elif choice == "4":
        print("bye bye")
        sys.exit(0)
    else:
        print("Bad choice.\n")
