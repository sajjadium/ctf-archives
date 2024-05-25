#!/usr/local/bin/python

import opcode

cod = bytes.fromhex(input("cod? "))
name = input("name? ")

if len(cod) > 20 or len(cod) % 2 != 0 or len(name) > 16:
    print("my memory is really bad >:(")
    exit(1)

# can't hack me if I just ban every opcode
banned = set(opcode.opmap.values())
for i in range(0, len(cod), 2):
    [op, arg] = cod[i:i + 2]
    if op in banned:
        print("your code is sus >:(")
        exit(1)
    if arg > 10:
        print("I can't count that high >:(")
        exit(1)

def f():
    pass

f.__code__ = f.__code__.replace(co_names=(name,), co_code=cod)

f()
