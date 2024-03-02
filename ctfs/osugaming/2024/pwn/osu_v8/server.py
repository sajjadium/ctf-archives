import sys
import os

sys.stdout.write("script size:\n")
sys.stdout.flush()
size = int(sys.stdin.readline().strip())
if size > 102400:
    sys.stdout.write("No way!\n")
    sys.stdout.flush()
    sys.exit(1)
sys.stdout.write("script:\n")
sys.stdout.flush()
script = sys.stdin.read(size)
with open(sys.argv[1], 'w') as f:
    f.write(script)

os.system("/home/ctf/d8 " + sys.argv[1])