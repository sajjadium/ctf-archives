#!/usr/bin/env python3

while True:
    allowed = set("abcdefghijklm")

    code = input(">>> ")

    broke_the_rules = False
    for c in code:
        if c.lower() not in allowed and c not in "\"'()=+:;. 1234567890":
            print(f"Character {c} not allowed!")
            broke_the_rules = True
            break
        allowed = set(chr((ord(a) - ord('a') + 1) % 26 + ord('a')) for a in allowed)

    if not broke_the_rules:
        exec(code)
