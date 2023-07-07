#!/usr/bin/env python3

import sys
import math
import functools
from PIL import Image
from random import randint
import string
from secret import flag, key, n

def pad(s, l):
	while len(s) < l:
		s += string.printable[randint(0, 61)]
	return s

def sox(n, d):
	x, y, t = 0, 0, d
	for s in range(n - 1):
		u = 1 & t // 2
		v = 1 & t ^ u
		x, y = spin(2**s, x, y, u, v)
		x += 2**s * u
		y += 2**s * v
		t = t // 4
	return x, y

def spin(n, x, y, u, v):
	if v == 0:
		if u == 1:
			x = n - 1 - x
			y = n - 1 - y
		x, y = y, x
	return x, y

def encrypt(msg, key, n):
	_msg = pad(msg, n ** 2)
	_msg, _key = [ord(_) for _ in _msg], [ord(_) for _ in key]
	img = Image.new('RGBA', (n, n), 'darkblue')
	pix = img.load()

	for _ in range(len(key)):
		w = len(_key)
		h = n**2 // w + 1
		arr = [[_msg[w*x + y] if w*x + y < n**2 else None for x in range(h)] for y in range(w)]
		_conf = sorted([(_key[i], i) for i in range(w)])
		_marshal = [arr[_conf[i][1]] for i in range(w)]
		_msg = functools.reduce(lambda a, r: a + _marshal[r], range(w), [])
		_msg = list(filter(lambda x: x is not None, _msg))
		_msg = [(_msg[_] + _key[_ % w]) % 256 for _ in range(n**2)]

	for d in range(n**2):
		x, y = sox(n, d)
		pix[x,y] = (_msg[d], _msg[d], _msg[d])
	keysum = sum(_key) if w > 0 else 0
	orient = keysum % 4
	img = img.rotate(90*orient)
	return img

assert len(key) == 3
img = encrypt(flag, key, n)
img.save('enc.png')