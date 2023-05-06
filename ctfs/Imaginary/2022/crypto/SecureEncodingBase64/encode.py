#!/usr/bin/env python3

from base64 import b64encode
from random import shuffle

charset = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='
shuffled = [i for i in charset]
shuffle(shuffled)

d = {charset[i]:v for(i,v)in enumerate(shuffled)}

pt = open("flag.txt").read()
while "\n\n\n" in pt:
    pt = pt.replace("\n\n\n", '\n\n')
while '  ' in pt:
    pt = pt.replace('  ', ' ')

assert all(ord(i)<128 for i in pt)

ct = bytes(d[i] for i in b64encode(pt.encode()))
f = open('out.txt', 'wb')
f.write(ct)
