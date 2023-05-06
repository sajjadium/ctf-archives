#!/usr/bin/env python3

# With credit/inspiration to the v8 problem in downUnder CTF 2020

import os
import subprocess
import sys
import tempfile

def p(a):
    print(a, flush=True)

MAX_SIZE = 20000
input_size = int(input("Provide size. Must be < 5k:"))
if input_size >= MAX_SIZE:
    p(f"Received size of {input_size}, which is too big")
    sys.exit(-1)
p(f"Provide script please!!")
script_contents = sys.stdin.read(input_size)
p(script_contents)
# Don't buffer
with tempfile.NamedTemporaryFile(buffering=0) as f:
    f.write(script_contents.encode("utf-8"))
    p("File written. Running. Timeout is 20s")
    res = subprocess.run(["./d8", f.name], timeout=20, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p("Run Complete")
    p(f"Stdout {res.stdout}")
    p(f"Stderr {res.stderr}")