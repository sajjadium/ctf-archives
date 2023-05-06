#!/usr/bin/env python
import hashlib
import string,random
import os
import sys

prefix = ''.join(random.choice(string.letters+string.digits) for _ in xrange(16))
difficulty = 18
zeros = '0' * difficulty

def is_valid(digest):
    digest = [ord(i) for i in digest]
    bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
    return bits[:difficulty] == zeros
sys.stdout.write("sha256({} + ???) == {}({})\nans:".format(prefix,zeros,difficulty))
sys.stdout.flush()
ans = sys.stdin.readline().strip()

if is_valid(hashlib.sha256(prefix+ans).digest()):
    sys.stdout.write("Great")
    sys.stdout.flush()
    os.system("/home/note/note")
    exit(0)
print "Failed"


