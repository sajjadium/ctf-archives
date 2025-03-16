#!/usr/local/bin/python
import sys, os
inpfile = open('/tmp/input', 'w')
while True:
    line = input()
    if line == "":
        break
    inpfile.write(line + "\n")
inpfile.close()
os.system('FLAG="$(cat flag.txt)" /k/k chall.k')
