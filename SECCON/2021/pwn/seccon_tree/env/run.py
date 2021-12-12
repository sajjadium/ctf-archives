#!/usr/bin/env python3.7
import sys
import os
import binascii
import re
import subprocess
import signal
import string
import urllib.request


LIBFILE = "seccon_tree.cpython-39-x86_64-linux-gnu.so"

def handler(_x,_y):
    sys.exit(-1)
signal.signal(signal.SIGALRM, handler)
signal.alarm(30)


def gen_filename():
    return '/prog/' + binascii.hexlify(os.urandom(16)).decode('utf-8')

def is_bad_str(code):
    code = code.lower()
    with open("banned_word") as f:
        l = f.read().strip("\n").split("\n")
    for s in l:
        if s in code:
            return True
    return False

def is_bad_char(code):
    for c in code:
       if c not in string.printable:
         return True
    return False

def is_bad(code):
    return is_bad_str(code) or is_bad_char(code)

place_holder = '/** code **/'
template_file = 'template.py'
MAX_SIZE = 10000

def main():
    print(f'Give me the source code url (where filesize < {MAX_SIZE}).')
    print(f"Someone says that https://transfer.sh/ is useful if you don't have your own server")
    url = input()
    if not url.startswith("http"):
        print("bad url")
        return False

    with urllib.request.urlopen(url) as res:
        code = res.read().decode("utf-8")

    if len(code) > MAX_SIZE:
        print('too long')
        return False

    if is_bad(code):
        print('bad code')
        return False

    with open(template_file, 'r') as f:
        template = f.read()

    filename = gen_filename() + ".py"
    with open(filename, 'w') as f:
        f.write(template.replace(place_holder, code))
    os.system(f'cp {LIBFILE} /prog/')
    os.system(f'timeout --foreground -k 20s 15s python3.9 {filename}')

main()
