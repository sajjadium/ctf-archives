#!/usr/bin/env -S python3 -u

import sys

def audit(name, args):
    if name not in ["exec", "compile", "builtins.input", "builtins.input/result"]:
        print("you did a bad thing")
        print("stay in jail forever")
        exit(0)

sys.addaudithook(audit)

while True:
    try:
        code = input(">>> ")
        exec(code)
    except Exception as e:
        print("Error occurred")
        exit(0)
