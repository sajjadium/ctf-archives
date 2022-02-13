#!/usr/bin/env python3

import os
import sys
import tempfile

def print(s):
    sys.stdout.write(s)
    sys.stdout.flush()

print("The number of files (max 3): ")

try:
    count = int(sys.stdin.readline().strip())
except:
    print("invalid input\n")
    exit()

if count > 3 or count <= 0:
    print("invalid input\n")
    exit()

tmppath = [0, 0, 0]
cmd = "./clamscan"

for i in range(count):
    print(f"file_size[{i}] (max 10000): ")

    try:
        file_size = int(sys.stdin.readline().strip())
    except:
        print("invalid input\n")
        exit()

    if file_size > 10000 or file_size <= 0:
        print("invalid input\n")
        exit()

    print(f"file_data[{i}]: ")
    file_data = sys.stdin.buffer.read(file_size)

    
    fd, tmppath[i] = tempfile.mkstemp()

    with open(tmppath[i], 'wb') as f:
        f.write(file_data)
    
    cmd += f' {tmppath[i]}'

os.system(cmd)

for i in range(count):
    os.unlink(tmppath[i])