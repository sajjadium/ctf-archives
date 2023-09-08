#!/usr/bin/env python3
from Crypto.Util.number import *
from shlex import quote
import subprocess, sys, signal


class RSA:
    def __init__(self, size):
        self.p = getPrime(size // 2)
        self.q = getPrime(size // 2)
        self.n = self.p * self.q
        self.e = getPrime(size // 2)
        self.d = pow(self.e, -1, (self.p - 1) * (self.q - 1))

    def sign(self, msg: bytes) -> int:
        m = bytes_to_long(msg)
        return pow(m, self.d, self.n)

    def verify(self, msg: bytes, sig: int) -> bool:
        return self.sign(msg) == sig


if __name__ == "__main__":
    signal.alarm(60)
    rsa = RSA(512)
    while True:
        print("1. Sign an echo command")
        print("2. Execute a signed command")
        print("3. Exit")
        choice = int(input("> "))
        if choice == 1:
            msg = input("Enter message: ")
            cmd = f"echo {quote(msg)}"
            sig = rsa.sign(cmd.encode())
            print("Command:", cmd)
            print("Signature:", sig)
        elif choice == 2:
            cmd = input("Enter command: ")
            sig = int(input("Enter signature: "))
            if rsa.verify(cmd.encode(), sig):
                subprocess.run(
                    cmd,
                    shell=True,
                    stdin=subprocess.DEVNULL,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                )
            else:
                print("Signature verification failed")
        elif choice == 3:
            break
