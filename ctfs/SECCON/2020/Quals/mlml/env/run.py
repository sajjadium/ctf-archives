#!/usr/bin/env python3.7
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

def is_bad_str(code):
    code = code.lower()
    # I don't like these words :)
    for s in ['__', 'open', 'read', '.', '#', 'external', '(*', '[', '{%', '{<', 'include']:
        if s in code:
            return True
    return False


def is_bad(code):
    return is_bad_str(code)


place_holder = '/** code **/'
template_file = 'template.ml'
EOF = 'SECCON'
MAX_SIZE = 10000


def main():
    print(f'Give me the source code(size < {MAX_SIZE}). EOF word is `{EOF}\'')
    size = 0
    code = ''
    while True:
        s = sys.stdin.readline()
        size += len(s)
        if size > MAX_SIZE:
            print('too long')
            return False
        idx = s.find(EOF)
        if idx < 0:
            code += s
        else:
            code += s[:idx]
            break

    if is_bad(code):
        print('bad code')
        return False

    with open(template_file, 'r') as f:
        template = f.read()

    filename = '/prog/prog.ml'
    with open(filename, 'w') as f:
        f.write(template.replace(place_holder, code))
    os.system(f'timeout --foreground -k 20s 15s ocamlopt {filename} -o /tmp/prog && timeout --foreground -k 10s 5s /tmp/prog')

main()

