#!/usr/bin/env python3

def encrypt(pt, PTALPHA, CTALPHA):
	ct = ''
	for ch in pt:
		i = PTALPHA.index(ch)
		ct += CTALPHA[i]
	return ct


PTALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
CTALPHA = open('CTALPHA.txt').read().strip()
FLAG = open('flag.txt').read().strip()

assert len(CTALPHA) == len(PTALPHA)
assert all(x in PTALPHA for x in FLAG)

enc_flag = encrypt(FLAG, PTALPHA, CTALPHA)

with open('flag.enc','w') as f:
	f.write(enc_flag)
	print('DONE')