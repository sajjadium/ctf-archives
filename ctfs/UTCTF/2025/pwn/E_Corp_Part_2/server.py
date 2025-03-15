#!/usr/bin/env python3 

import os
import subprocess
import sys
import tempfile

print("Size of Exploit: ", flush=True)
input_size = int(input())
print("Script: ", flush=True)
script_contents = sys.stdin.read(input_size)
with tempfile.NamedTemporaryFile(buffering=0) as f:
    f.write(script_contents.encode("utf-8"))
    print("Running. Good luck! ", flush=True)
    res = subprocess.run(["./d8", f.name], timeout=20, stdout=1, stderr=2, stdin=0)
    print("Done!", flush=True)
