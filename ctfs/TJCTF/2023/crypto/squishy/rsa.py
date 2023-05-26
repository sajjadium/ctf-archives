#!/usr/local/bin/python3.10 -u

import sys
import select
from Crypto.Util.number import bytes_to_long, getPrime


def input_with_timeout(prompt, timeout=10):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.buffer.readline().rstrip(b'\n')
    raise Exception


def sign(a):
    return pow(bytes_to_long(a), d, n)


def check(a, s):
    return bytes_to_long(a) == pow(s, e, n)


e = 65537
users = {b"admin"}

p = getPrime(1000)
q = getPrime(1000)
n = p * q
d = pow(e, -1, (p - 1) * (q - 1))


print(n)

while True:
    cmd = input("Cmd: ")
    if cmd == "new":
        name = input_with_timeout("Name: ")
        if name not in users:
            users.add(name)
            print(name, sign(name))
        else:
            print("Name taken...")
    elif cmd == "login":
        name = input_with_timeout("Name: ")
        sig = int(input_with_timeout("Sign: ").decode())
        if check(name, sig) and name in users:
            if name == b"admin":
                print("Hey how'd that happen...")
                print(open("flag.txt", "r").read())
            else:
                print("No admin, no flag")
        else:
            print("Invalid login.")

    else:
        print("Command not recognized...")
