#!/usr/local/bin/python3
import string
import html

code = input()

if any(c not in string.printable for c in code):
    print("no tomfoolery!")
    exit()

if "e" in code or "E" in code:
    print("no 'e'!")
    exit()

print(html.escape(repr(eval(code, {"__builtins__": {}}))))
