#!/usr/bin/python3

from Crypto.Util.number import *
from Crypto.Random import random

from redacted import FLAG

import signal

BANNER = (
    "          \n"
    '          (       "     )   Just a small dash of OTP\n'
    "           ( _  *           And the FLAG is lost forever!\n"
    "              * (     /      \\    ___\n"
    '                 "     "        _/ /\n'
    "                (   *  )    ___/   |\n"
    "                  )   \"     _ o)'-./__\n"
    "                 *  _ )    (_, . $$$\n"
    "                 (  )   __ __ 7_ $$$$\n"
    "                  ( :  { _)  '---  $\\\n"
    "              _____'___//__\\   ____, \\\n"
    "              )           ( \\_/ _____\\_\n"
    "            .'             \\   \\------''.\n"
    "            |='           '=|  |         )\n"
    "            |               |  |  .    _/\n"
    "             \\    (. ) ,   /  /__I_____\\\n"
    "             '._/_)_(\\__.'   (__,(__,_]\n"
    "             @---()_.'---@\n"
)


def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    myprint("Time out!")
    exit(0)


class Cipher:
    BITS = 256

    def __init__(self):
        self.p = getPrime(Cipher.BITS)
        self.q = getPrime(Cipher.BITS)
        self.n = self.p * self.q
        self.e = 0x10001

        phi = (self.p - 1) * (self.q - 1)
        self.d = inverse(self.e, phi)

    def encrypt(self, pt):
        ct = pow(pt, self.e, self.n)
        return bin(ct)[2:]

    def decrypt_lol(self, ct):
        pt = pow(ct, self.d, self.n)

        pt_len = len(bin(pt)[2:])
        dec = list(map(int, bin(pt)[2:]))
        otp_key = list(map(int, bin(random.getrandbits(pt_len))[2:]))

        for i in range(len(otp_key)):
            dec[i] ^= otp_key[i]

        return "".join(list(map(str, dec)))


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    myprint(BANNER)

    cipher = Cipher()

    myprint(f"N = {cipher.n}")
    myprint(f"e = {cipher.e}")
    myprint(f"enc(flag) = {cipher.encrypt(bytes_to_long(FLAG))}\n")

    while True:
        user_ct = int(input("Enter ciphertext: "), 2)
        pt = cipher.decrypt_lol(user_ct)
        myprint(f"Decrypted: {pt}")


if __name__ == "__main__":
    main()
