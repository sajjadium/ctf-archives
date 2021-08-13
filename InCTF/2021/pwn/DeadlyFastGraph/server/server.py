#!/usr/bin/python3

import sys
import tempfile
import os

print ("Enter the file size and then the file >>")
size = int(input())
assert(size < 1024*1024) #1MB max
script = sys.stdin.read(size) # reads one byte at a time, similar to getchar()

temp = tempfile.mktemp()
with open(temp, "w") as f:
        f.write(script)

os.system("./jsc --useConcurrentJIT=false "+temp)
