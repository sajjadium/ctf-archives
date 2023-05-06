#!/usr/bin/env python3
import sys
import os
import binascii
import re
import subprocess
import signal
import urllib.request

def handler(x, y):
    sys.exit(-1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(30)

def is_bad_str(code):
    code = code.lower()
    # I don't like these words :)
    for s in ['__', 'open', 'read', '.', '#', 'external', '(*', '[', '{%', '{<',
            'include', 'unsafe', 'match']:
        if s in code:
            return True
    return False


def is_bad(code):
    return is_bad_str(code)

place_holder = '/** code **/'
template_file = 'template.ml'
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

    filename = '/prog/prog.ml'
    with open(filename, 'w') as f:
        f.write(template.replace(place_holder, code))
    os.system(f'timeout --foreground -k 20s 15s ocamlc {filename} -o /tmp/prog && timeout --foreground -k 10s 5s /tmp/prog')

main()
