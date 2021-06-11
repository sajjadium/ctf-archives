#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flag import flag

def xor(u, v):    
	return ''.join(chr(ord(cu) ^ ord(cv)) for cu, cv in zip(u, v))

u = flag
v = flag[1:] + flag[0]

enc = open('flag.enc', 'w')
enc.write(xor(u, v))
enc.close()
