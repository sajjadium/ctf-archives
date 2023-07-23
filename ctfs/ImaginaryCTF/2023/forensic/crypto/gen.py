#!/usr/bin/env python3

import os

key = [line.strip() for line in open("private.pem", "rb").readlines()[1:-1]]
c = open("core.raw", "rb").read() # coredump of `python3 script.py`

for line in key:
  c = c.replace(line, b"A"*len(line))

open("core", "wb").write(c)

os.system("openssl rsautl -encrypt -inkey public.pem -pubin -in flag.txt -out flag.enc")
