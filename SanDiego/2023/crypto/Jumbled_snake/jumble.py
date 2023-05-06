#! /usr/bin/env python3
# Need print_flag.py (secret) in the same directory as this file
import print_flag
import os
import secrets
import string

def get_rand_key(charset: str = string.printable):
    chars_left = list(charset)
    key = {}
    for char in charset:
        val = secrets.choice(chars_left)
        chars_left.remove(val)
        key[char] = val
    assert not chars_left
    return key

def subs(msg: str, key) -> str:
    return ''.join(key[c] for c in msg)

with open(os.path.join(os.path.dirname(__file__), 'print_flag.py')) as src, open('print_flag.py.enc', 'w') as dst:
    key = get_rand_key()
    print(key)
    doc = print_flag.decode_flag.__doc__
    assert doc is not None and '\n' not in doc
    dst.write(doc + '\n')
    dst.write(subs(src.read(), key))
