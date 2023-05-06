#!/usr/bin/python3
import sys
import os
import binascii
import re
import subprocess
import signal

def handler(x, y):
    sys.exit(-1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(30)

def gen_filename():
    return '/tmp/' + binascii.hexlify(os.urandom(16)).decode('utf-8')

EOF = 'ASIS-CTF'
MAX_SIZE = 10000

def main():
    print(f'Give me the source code(size < {MAX_SIZE}). EOF word is `{EOF}\'')
    sys.stdout.flush()
    size = 0
    code = ''
    while True:
        s = sys.stdin.readline()
        size += len(s)
        if size > MAX_SIZE:
            print('too long')
            sys.stdout.flush()
            return False
        idx = s.find(EOF)
        if idx < 0:
            code += s
        else:
            code += s[:idx]
            break
    filename = gen_filename() + ".js"
    with open(filename, 'w') as f:
        f.write(code)
    os.close(1)
    os.close(2)
    os.system(f'./run.sh {filename}')
main()
