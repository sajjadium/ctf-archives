#!/usr/local/bin/python

import subprocess
from binascii import unhexlify

i = input()

p = subprocess.run(["./drive"], input=unhexlify(i), capture_output=True)

print(p.stdout.decode())
