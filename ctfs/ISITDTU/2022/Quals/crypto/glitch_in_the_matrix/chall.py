#!/usr/bin/env python3
from secret import SECRET_BASIS
from secrets import token_hex
import random
import os

assert len(SECRET_BASIS) == len(SECRET_BASIS[0]) == 128

def f(M: list[list[int]], C: list[int]) -> list[int]:
    v = [0] * len(M[0])
    for c, m in zip(C, M):
        if c:
            v = [x ^ y for x, y in zip(v, m)]
    return v

def random_bits(n: int) -> list[int]:
    return list(map(int, bin(random.getrandbits(n))[2:].rjust(n, "0")))

def encrypt(message: bytes) -> str:
    M = [b for c in message for b in map(int, "{:08b}".format(c))]
    ct = []
    for bit in M:
        C = random_bits(64)
        v = f(SECRET_BASIS[:64], C) if bit else f(SECRET_BASIS[64:], C)
        ct.extend(v)
    ct = "".join(map(str, ct))
    return bytes([int(ct[i:i+8], 2) for i in range(0, len(ct), 8)]).hex()

def decrypt(ciphertext: str) -> bytes:
    # TODO: implement this pls
    pass

def action_prompt() -> int:
    print('''============= MENU =============
    1. Have a guess
    2. Get ciphertext
    3. Change password
    4. Quit
================================\n''')
    try:
        option = int(input("Your option> "))
    except:
        return None
    return option

def chall():
    try:
        password = token_hex(8)
        while True:
            option = action_prompt()
            if option == 1:
                user_password = input("Input your password (hex): ")
                if user_password == password:
                    print(f"Is taking the red pill worth it? Here is the truth that you want: {os.environ['FLAG']}.")
                else:
                    print("Guess you can't escape the matrix after all.")
                break
            elif option == 2:
                print(f"Leaky ciphertext: {encrypt(bytes.fromhex(password))}")
            elif option == 3:
                print("Generating super secure password ...")
                password = token_hex(8)
            elif option == 4:
                print("Maybe the truth is not that important, huh?")
                break
            else:
                print("Invalid option.")
            print("\n")
    except:
        print("An error occured!")

chall()
