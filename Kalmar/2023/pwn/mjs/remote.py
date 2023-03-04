#!/usr/bin/env python3
import subprocess

print("Welcome to mjs.")
print("Please give input. End with \"EOF\":")

s = ""
try:
    while True:
        _s = input()
        if _s == 'EOF':
            break
        s += _s
except EOFError:
    pass

p = subprocess.Popen(["./mjs", "-e", s])
p.wait()

