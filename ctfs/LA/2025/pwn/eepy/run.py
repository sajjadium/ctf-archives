#!/usr/local/bin/python

import os
import time
import base64
import string
import subprocess

inp = base64.b64decode(input())[:0xe]
with open("vuln", "rb") as file:
    data = bytearray(file.read())
    data[0x1050:0x105e] = inp.ljust(0xe, b"\x00")
    file.close()
with open("/tmp/vuln", "wb") as file:
    file.write(data)
    file.close()

zzz = 0
args = ""
while len(args) < 0x22fed:
    line = input()
    if not line:
        break
    for c in line:
        if c not in string.printable:
            exit()
        if c == "Z":
            zzz += 1
        elif c == "A":
            print("too awake")
            exit()
        elif c == "\n":
            continue
        args += c
if len(args) > 0x22fed or zzz < 0x11f6f:
    print("not enough eepy")
    exit()

print("ZZZZzzzzZZZZzzzzZZZZzzzz", flush=True)
os.chmod("/tmp/vuln", 0o777)
p = subprocess.Popen(
    ["/tmp/vuln"] + args.split(),
    env={},
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(10)
