#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes

import hashlib
import os
import signal

BANNER = ("                              \n"
          "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠛⠛⠛⠛⠛⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
          "⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠙⠷⣄⠀⠀⠀⠀⠀⠀⠀⠀\n"
          "⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⠀⠀⠀⠀\n"
          "⠀⠀⠀⠀⠀⠀⠀⡿ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⠀⠀\n"
          "⠀⠀⠀⠀⠀⠀⢀⡿⠀⠀⢀⣀⣤⡴⠶⠶⢦⣤⣀⡀⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀\n"
          "⠀⠀⠀⠀⠀⠀⠘⣧⡀⠛⢻⡏⠀⠀⠀⠀⠀⠀⠉⣿⠛⠂⣼⠇⠀⠀⠀⠀⠀⠀\n"
          "⠀⠀⠀⠀⢀⣤⡴⠾⢷⡄⢸⡇⠀⠀⠀⠀⠀⠀⢀⡟⢀⡾⠷⢦⣤⡀⠀⠀⠀⠀\n"
          "⠀⠀⠀⢀⡾⢁⣀⣀⣀⣻⣆⣻⣦⣤⣀⣀⣠⣴⣟⣡⣟⣁⣀⣀⣀⢻⡄⠀⠀⠀\n"
          "⠀⠀⢀⡾⠁⣿⠉⠉⠀⠀⠉⠁⠉⠉⠉⠉⠉⠀⠀⠈⠁⠈⠉⠉⣿⠈⢿⡄⠀⠀\n"
          "⠀⠀⣾⠃⠀⣿⠀⠀⠀⠀⠀⠀⣠⠶⠛⠛⠷⣤⠀⠀⠀⠀⠀⠀⣿⠀⠈⢷⡀⠀\n"
          "⠀⣼⠃⠀⠀⣿⠀⠀⠀⠀⠀⢸⠏⢤⡀⢀⣤⠘⣧⠀⠀⠀⠀⠀⣿⠀⠀⠈⣷⠀\n"
          "⢸⡇⠀⠀⠀⣿⠀⠀⠀⠀⠀⠘⢧⣄⠁⠈⣁⣴⠏⠀⠀⠀⠀⠀⣿⠀⠀⠀⠘⣧\n"
          "⠈⠳⣦⣀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠻⠶⠶⠟⠀⠀⠀⠀⠀⠀⠀⣿⠀⢀⣤⠞⠃\n"
          "⠀⠀⠀⠙⠷⣿⣤⣤⣤⣤⣤⣠⣤⣤⣤⣤⣀⣤⣠⣤⣀⣤⣤⣄⣿⡶⠋⠁⠀⠀\n"
          "⠀⠀⠀⠀⠀⢿⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣿⠀⠀⠀⠀⠀\n")


def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    print("Time out!")
    exit(0)


def hack_detected():
    myprint("Hack detected... go away!")
    exit(1)


def bxor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])


def hash(num):
    return hashlib.sha256(long_to_bytes(num)).digest()


class LCG:
    def __init__(self, a, b, m):
        self.a = a
        self.b = b
        self.m = m
        self.state = bytes_to_long(os.urandom(32))

    def next(self):
        self.state = (self.a * self.state + self.b) % self.m
        return self.state


class CustomCipher:
    N_KEYS = 16

    def __init__(self, keygen):
        self.keygen = keygen
        self.keys = [hash(keygen.next()) for _ in range(self.N_KEYS)]

        if len(set(self.keys)) < self.N_KEYS // 2:
            hack_detected()

    def encrypt(self, pt):
        L = [pt[:32]]
        R = [pt[32:]]

        for (i, ki) in enumerate(self.keys):
            iv = bxor(self.keys[i][16:], self.keys[(
                i + self.N_KEYS // 2) % self.N_KEYS][:16])
            F = AES.new(ki, AES.MODE_CBC, iv=iv)
            l, r = R[-1], bxor(L[-1], F.encrypt(R[-1]))
            if i + 1 == self.N_KEYS // 2:
                l, r = r, l
            L.append(l)
            R.append(r)

        return L[-1] + R[-1]

    def tamper(self, a, b, c):
        for idx in [a, b, c]:
            if not 1 <= idx <= self.N_KEYS:
                hack_detected()

        self.keys[a - 1] = bxor(self.keys[b - 1], self.keys[c - 1])


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    myprint(BANNER)

    myprint(
        "\"Don't roll out your own crypto!\" is just a piece of advice for the weak.")
    myprint("    * We have a strong team of world renowned researchers!")
    myprint("    * We are not weak!")
    myprint("    * We are not afraid of hackers!")
    myprint("    * We are so confident we've opened some backdoors!")
    myprint("")
    myprint("Enjoy wasting your time on this...")
    myprint("")

    m = 2 ** 256
    a = int(input("Insert key generator b[a]ckdoor: ")) % m
    b = int(input("Insert key generator [b]ackdoor: ")) % m

    cipher = CustomCipher(LCG(a, b, m))

    for i in range(1, 13):
        myprint(
            f"[{i}/12] Wanna tamper with the keys [(a, b, c) --> ka = kb ^ kc])?")

        s = input("> ")

        if s == "no":
            continue

        a, b, c = map(int, s.split())
        cipher.tamper(a, b, c)

    flag = open("flag.txt", "rb").read()
    assert(len(flag) == 64)

    flag_ct = cipher.encrypt(flag).hex()

    myprint(f"Here is your encrypted flag: {flag_ct}")


if __name__ == '__main__':
    main()
