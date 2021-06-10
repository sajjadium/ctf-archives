#!/usr/bin/python -u
# encoding: utf-8

import random, string, subprocess, os, sys
from hashlib import sha256

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def proof_of_work():
    chal = ''.join(random.choice(string.letters+string.digits) for _ in xrange(16))
    print chal
    sol = sys.stdin.read(4)
    if len(sol) != 4 or not sha256(chal + sol).digest().startswith('\0\0\0'):
        exit()


def exec_serv(name, payload):
    p = subprocess.Popen(name, stdin=subprocess.PIPE, stdout=file('/dev/null','w'), stderr=subprocess.STDOUT)
    p.stdin.write(payload)
    p.wait()

if __name__ == '__main__':
    proof_of_work()
    payload = sys.stdin.read(0x100)
    exec_serv('./babystack', payload)
