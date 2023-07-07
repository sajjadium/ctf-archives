#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def base(n, l):
    D = []
    while n > 0:
        n, r = divmod(n, l)
        D.append(r)
    return ''.join(str(d) for d in reversed(D)) or '0'

def asiv_prng(seed):
	l = len(seed)
	_seed = base(bytes_to_long(seed), 3)
	_l = len(_seed)
	R = [[getRandomRange(0, 3) for _ in range(_l)] for _ in range(_l**2)]
	S = []
	for r in R:
		s = 0
		for _ in range(_l):
			b = ((int(r[_]) + int(_seed[_])) % 3) % 2
			s = s ^ b
		S.append(s)
	print(len(S))
	return R, S

seed = flag.lstrip(b'CCTF{').rstrip(b'}')
R, S = asiv_prng(seed)

f = open('output.txt', 'w')
f.write(f'R = {R}\nS = {S}')
f.close()