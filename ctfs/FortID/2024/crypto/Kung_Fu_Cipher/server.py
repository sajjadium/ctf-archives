from Crypto.Util.number import *
from sage.all import *
from redacted import FLAG

import random
import signal

BANNER = (
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣦⣤⣖⣶⣒⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣾⣿⣿⣿⣿⣿⣶⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⢜⡛⠈⠛⢙⣃⠙⢿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⢟⠀⠀⠹⠀⠀⠘⠃⣸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⢀⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡈⠷⠀⠀⠀⠁⠀⠹⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⢀⣿⣏⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠛⠛⠛⢦⣍⣃⣀⡴⠂⠀⣽⠙⠲⢤⣀⠀⠀⠀⠀⠀⠀⠀This is a sparing program...  ⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⢸⡘⣿⣾⣇⠀⠀⠀⠀⠀⠀⠀⢠⡾⠁⠀⠀⠀⠀⡀⠙⢇⠁⠀⠀⠀⡿⠀⠀⠀⠈⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠸⡅⠻⠯⣿⠀⠀⠀⠀⠀⠀⣠⠏⣀⠀⠀⠀⠀⠀⠳⡄⠈⠳⡄⠀⣰⠃⢰⠆⠀⠀⢸⡇⠀⠀⠀It has the same basic rules as any⠀⠀ \n"
    "⠀⠀⠀⠀⠀⠉⠳⣆⠈⢻⣄⠀⠀⢀⡞⠁⠀⠘⢦⠀⠀⠀⠀⠀⠙⣆⠀⠙⢦⠏⢀⡞⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀ other cryptographic program. ⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢨⡷⣾⠈⠳⣤⠟⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠈⠃⢀⡞⠀⣸⠃⠀⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠸⣟⠁⠀⠀⠈⠳⣄⡀⠀⠀⢀⡼⠆⠀⠀⠀⠀⠀⢀⡜⠀⣰⠇⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀What you must learn is that some⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠀⠈⠉⢀⡴⠋⣆⠀⠀⠀⠀⠀⢀⡞⠀⣠⠏⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀of these rules can be bent,⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⣠⠖⠉⠀⠀⢹⡀⠀⠀⠀⢀⡞⠀⣠⠏⠀⠀⠀⠀⠀⣼⣓⣶⣶⣦⠀⠀⠀⠀⠀ others can be broken.⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⢷⠀⠀⣠⠋⠀⡰⠏⠀⠀⠀⠀⠀⠀⣿⢹⡶⣾⡿⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣾⣥⣄⡈⠁⠀⠀⠀⠀⠀⠀⠀⡏⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠛⠛⢿⣿⣿⣿⣿⣶⣶⣤⣤⣤⣼⠁⠀⠀⠀⠀⠀OPTIONS:                 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠃⠀⠀⠀⠀⠈⠉⠉⠛⢻⣿⣿⣿⠛⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠁⣰⡆⠀⠀⠀⠀⠀⠀⠀⣾⣿⠀⢿⣧⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀1) Encrypt the FLAG  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣡⠞⠁⢣⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠸⣿⣇⠀⠈⢣⡀⠀⠀⠀⠀⠀2) Encrypt arbitrary plaintext⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠟⠁⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⢿⣿⡀⠀⣀⣷⠀⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⣿⣿⣆⡀⠼⣿⣿⠉⠉⠈⢦⠀⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠛⢻⠟⠛⠛⠛⠋⠉⠙⠛⢦⠀⣿⣿⡆⠀⠀⠈⢷⠀⠀⠀⠀   What are you waiting for?⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠈⠀⠀⠀⠀⠈⢳⡀⠀⠀You're a better hacker than this\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠈⢳⡄⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⢀⡾⠁⠀   Don't think you are,⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⣴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⣼⠃⠀⠀      KNOW YOU ARE!  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡁⠀⠀⠀⠀⣸⣻⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠘⠉⡏⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⢈⡇⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⢀⡼⠃⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⢀⣽⠦⣤⡀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠋⠛⡶⠤⣤⣀⣸⡿⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⣀⣀⡴⠖⠉⠀⠀⠀⠉⠑⡶⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⢧⡀⠀⠀⠁⠀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⢻⣯⣥⡀⠀⣤⠤⠤⠤⠴⠞⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢉⣳⣤⣄⡀⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠙⠓⠚⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠓⠒⠚⠛⠋⠁⠀⠀⠀                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
)


def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    myprint("Time out!")
    exit(0)


class KungFuCipher:
    BITS = 512

    def __init__(self):
        rng = random.SystemRandom()
        self.p = KungFuCipher.get_prime(rng)
        self.q = KungFuCipher.get_prime(rng)
        self.n = self.p * self.q
        self.e = getPrime(100)

    def get_prime(rng):
        DIGITS = 80
        while True:
            ret = 0
            for _ in range(DIGITS):
                ret *= 10
                ret += rng.choice([5, 7, 9])
            if isPrime(ret):
                return ret

    def encrypt(self, pt):
        def mul(A, B, mod):
            return (A * B).apply_map(lambda x: x % mod)

        M = matrix(ZZ, 2, 2, pt).apply_map(lambda x: x % self.n)
        C = identity_matrix(ZZ, M.nrows())

        e = self.e
        while e > 0:
            if e & 1:
                C = mul(C, M, self.n)
            M = mul(M, M, self.n)
            e //= 2

        return C


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    myprint(BANNER)

    cipher = KungFuCipher()

    myprint(f"n = {hex(cipher.n)}\n")

    assert len(FLAG) % 4 == 0

    k = len(FLAG) // 4
    pt = [bytes_to_long(FLAG[i * k : (i + 1) * k]) for i in range(4)]

    flag_ct = cipher.encrypt(pt)

    for _ in range(10):
        action = input("> ")
        if action == "1":
            for i in range(2):
                for j in range(2):
                    myprint(f"ct[{i}][{j}] = {hex(flag_ct[i][j])}")
        elif action == "2":
            user_pt = []
            for i in range(2):
                for j in range(2):
                    try:
                        x = int(input(f"pt[{i}][{j}] = "), 16)
                    except Exception as _:
                        myprint("kthxbai")
                        exit(0)
                    user_pt.append(x)

            user_ct = cipher.encrypt(user_pt)
            for i in range(2):
                for j in range(2):
                    myprint(f"ct[{i}][{j}] = {hex(user_ct[i][j])}")
            pass
        else:
            break

    myprint("kthxbai")


if __name__ == "__main__":
    main()
