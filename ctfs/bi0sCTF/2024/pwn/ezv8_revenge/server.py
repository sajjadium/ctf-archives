#!/usr/bin/python3

import sys
import tempfile
import os

sys.stdout.write("File size >> ")
sys.stdout.flush()
size = int(sys.stdin.readline().strip())
if size > 1024*1024:
    sys.stdout.write("Too large!")
    sys.stdout.flush()
    sys.exit(1)
sys.stdout.write("Data >> ")
sys.stdout.flush()
script = sys.stdin.read(size)

filename = tempfile.mktemp()
with open(filename, "w") as f:
    f.write(script)

os.system("./d8 " + filename)
