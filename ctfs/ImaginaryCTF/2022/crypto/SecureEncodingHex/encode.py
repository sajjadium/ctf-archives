#!/usr/bin/env python3

from random import shuffle

charset = '0123456789abcdef'
shuffled = [i for i in charset]
shuffle(shuffled)

d = {charset[i]:v for(i,v)in enumerate(shuffled)}

pt = open("flag.txt").read()
assert all(ord(i)<128 for i in pt)

ct = ''.join(d[i] for i in pt.encode().hex())
f = open('out.txt', 'w')
f.write(ct)
