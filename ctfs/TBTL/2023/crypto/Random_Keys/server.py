#!/usr/bin/python3

from Crypto.Util.number import *

import os
import signal

BANNER = ("                                                                             \n"
          "                                                             ######          \n"
          "                                                         ####******####      \n"
          "                                                       ##**************##    \n"
          "                                                     ##****##########****##  \n"
          "                                                     ##****##      ##****##  \n"
          "     ################################################****##          ##****##\n"
          "     ##**************************************************##          ##****##\n"
          "       ##****##****##****############################****##          ##****##\n"
          "         ####  ####  ####                            ##****##      ##****##  \n"
          "                                                     ##****##########****##  \n"
          "                                                       ##**************##    \n"
          "                                                         ####******####      \n"
          "                                                             ######          \n")


def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    print("Time out!")
    exit(0)


class LCG:
    def __init__(self):
        self.m = 128
        self.state = bytes_to_long(os.urandom(1))
        self.a = bytes_to_long(os.urandom(1))
        self.b = bytes_to_long(os.urandom(1))

    def next(self):
        self.state = (self.a * self.state + self.b) % self.m
        return self.state


class RSA:
    BITS = 512

    def __init__(self):
        self.primes = [getPrime(self.BITS) for _ in range(128)]
        self.gen = LCG()

    def encrypt(self, msg):
        p = self.primes[self.gen.next()]
        q = self.primes[self.gen.next()]
        N = p * q
        e = 0x10001
        return (N, e, hex(pow(msg, e, N)))


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    myprint(BANNER)

    myprint("Try to defeat our new encryption service using a chosen plaintext attack with at most 10 queries:")
    myprint("    1) Encrypt arbitrary message")
    myprint("    2) Encrypt flag and exit")
    myprint("")

    print("Initializing service... ", end="", flush=True)
    cipher = RSA()
    myprint("DONE!")
    myprint("")

    for _ in range(10):
        action = input("> ")
        if action == '1':
            message = bytes_to_long(bytes.fromhex(input("Message (hex): ")))
            result = cipher.encrypt(message)
            myprint(f"Result (N, e, ct): {result}")
        elif action == '2':
            flag = bytes_to_long(open("flag.txt", "rb").read())
            result = cipher.encrypt(flag)
            myprint(f"Result (N, e, ct): {result}")
            exit(0)


if __name__ == '__main__':
    main()
