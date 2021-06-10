import sys
import tempfile
import os

print("How many bytes is your exploit? (1MB max)", flush=True) 
size = int(input())
assert(size < 1024*1024)
print("Please minify and copy paste your exploit script", flush=True)
script = sys.stdin.read(size) # reads one byte at a time

temp = tempfile.mktemp()
with open(temp, "w") as f:
    f.write(script)

os.system("/home/ctf/d8/d8 "+temp)
