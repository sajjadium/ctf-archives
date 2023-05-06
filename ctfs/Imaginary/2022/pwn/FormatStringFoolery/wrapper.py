#!/usr/bin/env python3

from subprocess import PIPE, Popen
import sys

flag = open("flag.txt", "rb").read().strip()

# thanks to pepsipu for the idea

sys.stdout.write("Enter input:\n")
inp = sys.stdin.readline().encode()
for _ in range(10):
  p = Popen("./fmt_foolery", stdin=PIPE, stdout=PIPE, stderr=PIPE)
  if flag in p.communicate(input=inp, timeout=4)[0]:
    sys.stdout.write(f"passed round {_}\n")
  else:
    sys.stdout.write(f"failed round {_}\n")
    exit()

sys.stdout.write(f"Your flag is {flag}\n")
