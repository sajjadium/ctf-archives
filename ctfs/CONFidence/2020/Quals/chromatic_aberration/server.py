import sys
import tempfile
import os
import pow

pow.check_pow()

print ("Give me file\n") 
size = int(input())
assert(size < 1024*1024) #1MB max
script = sys.stdin.read(size) # reads one byte at a time, similar to getchar()

temp = tempfile.mktemp()
with open(temp, "w") as f:
	f.write(script)

os.system("/app/bin/d8 "+temp)
