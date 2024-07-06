import os, sys
q, y = os.urandom(16), 0
for x in sys.stdin.buffer.read(): sys.stdout.buffer.write(bytes([q[y % 16] ^ x])); y = x