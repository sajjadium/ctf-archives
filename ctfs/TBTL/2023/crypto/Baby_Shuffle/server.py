#!/usr/bin/python3

from Crypto.Util.number import *

import os
import signal

BABY_FLAG = ("                                           .@@@@@.\n"
             "                                          /       \\\n"
             "                                         /  6 6    \\\n"
             "                                        (    ^     ,)\n"
             "                                         \\   c     /-._\n"
             "                                          `._____.'    `--.__\n"
             "                                                 \\ /         `/``\"\"\"'-.\n"
             "                                                  Y    7     /         :\n"
             "                                                  |   /     |  .--.     :\n"
             "          *****   *****   *****   *****          /  /__     \\/    `.__.:.____.-.\n"
             "          * G *   * F *   * L *   * A *         /  / / `\"\"\"`/    .-\"..____.-.   \\\n"
             "          *****   *****   *****   *****     _.-'  /_/      (                 \-. \\\n"
             "                                            `=----'          `----------'\"\"`-. \ `\"\n")


def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    myprint("Time out!")
    exit(0)


class RSA:
    BITS = 512

    def __init__(self):
        self.p = getPrime(self.BITS)
        self.q = getPrime(self.BITS)
        self.n = self.p * self.q
        self.e = 17

    def pubkey(self):
        return (self.n, self.e)

    def encrypt(self, m):
        return pow(m, self.e, self.n)


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    myprint(BABY_FLAG)

    myprint("This challenge is unbreakable! Just listen to the setup:")
    myprint("    1) We give you the encrypted secret FLAG")
    myprint("    2) We give the FLAG to the youngest TBTL member")
    myprint("    3) They shuffle the FLAG")
    myprint("    4) We give you the encrypted shuffled FLAG")
    myprint(
        "    5) We laugh at you for wasting your time trying to figure out the FLAG :)")
    myprint("")
    myprint("Our newest member is still a baby... they are good at shuffling, right?")
    myprint("")
    myprint("")

    cipher = RSA()

    flag = open("flag.txt", "r").read().strip()
    shuffled_flag = flag[-1] + flag[:-1]

    assert(len(flag) == 61)

    myprint(f"(N, e) = ({cipher.n}, {cipher.e})")

    m1 = bytes_to_long(flag.encode("utf-8"))
    m2 = bytes_to_long(shuffled_flag.encode("utf-8"))

    c1 = cipher.encrypt(m1)
    c2 = cipher.encrypt(m2)

    myprint(f"c1 = {c1}")
    myprint(f"c2 = {c2}")

if __name__ == '__main__':
    main()
