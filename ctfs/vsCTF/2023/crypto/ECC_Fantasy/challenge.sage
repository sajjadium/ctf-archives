from random import getrandbits

load("utils.sage")

with open("flag.txt", "rb") as f:
    flag = f.read()

BITS = 256
FANCY = 1337
MENU = """===== Menu =====
1. Generate
2. Flag
3. Exit
================"""

try:
    i = 0
    while i < 100:
        i += 1
        print(MENU)
        c = int(input("Your choice: ").strip())
        if c == 1:
            E, p = gen_curve(BITS + 32)
            P = E.random_point()
            s = getrandbits(BITS)
            Q = s * P
            print(f"p = {p}")
            print(f"P = {P}")
            print(f"Q = {Q}")
        elif c == 2:
            print("No more fantasy for you.")
            secret = int.from_bytes(flag, "big") * getrandbits(FANCY) + getrandbits(FANCY)
            print(f"Secret is given to you: {hex(secret)}")
            break
        else:
            break
except:
    exit(1)