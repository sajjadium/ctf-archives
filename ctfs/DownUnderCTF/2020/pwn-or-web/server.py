#!/usr/bin/env python3
import os
import sys
import subprocess
import tempfile

MAX_SIZE = 100 * 1024

script_size = int(input("Enter the size of your exploit script (in bytes, max 100KB): "))
assert script_size < MAX_SIZE
print("Minify your exploit script and paste it in: ")
contents = sys.stdin.read(script_size)

tmp = tempfile.mkdtemp(dir="/tmp", prefix=bytes.hex(os.urandom(8)))
index_path = os.path.join(tmp, "exploit.js")
with open(index_path, "w") as f:
    f.write(contents)

sys.stderr.write("New submission at {}\n".format(index_path))

subprocess.run(["/home/ctf/d8", index_path], stderr=sys.stdout)

# Cleanup
os.remove(index_path)
os.rmdir(tmp)
