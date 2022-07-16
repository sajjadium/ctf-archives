#!/usr/bin/env python3

import random, sys
from secret import skey, flag

Omega = [
		0x4e, 0x96, 0xfd, 0x7d, 0x8d, 0xf6, 0xdb, 0x33, 0x1e, 0x16, 0x9b, 0x6a, 0xe2, 0xc9, 0xa9, 0xe0, 
		0x34, 0xe6, 0x86, 0xd6, 0x52, 0x02, 0x25, 0x1f, 0x23, 0xdf, 0xd5, 0x12, 0x45, 0x6b, 0x6f, 0x4d, 
		0x31, 0x77, 0x09, 0xbf, 0x93, 0xca, 0x4b, 0xef, 0xee, 0x7c, 0x53, 0x1a, 0xc8, 0xea, 0x9d, 0xda, 
		0x32, 0xa4, 0x11, 0x7b, 0xd8, 0x3f, 0x13, 0x57, 0x75, 0xcb, 0x37, 0x9a, 0x83, 0xa5, 0x3e, 0xd3, 
		0x4a, 0x1d, 0x29, 0xb9, 0x18, 0x27, 0x2d, 0x0f, 0x15, 0x0d, 0x66, 0xae, 0xf5, 0xfa, 0x08, 0x9f, 
		0xc6, 0x55, 0xa0, 0xb7, 0x28, 0x0e, 0xf4, 0x01, 0x04, 0x46, 0xf9, 0x39, 0xe3, 0x7f, 0x5e, 0x61, 
		0x40, 0x26, 0xec, 0xb6, 0x14, 0xf0, 0x59, 0x50, 0xcf, 0x3a, 0x8b, 0x43, 0xaf, 0x10, 0xe5, 0xe8, 
		0x03, 0xbd, 0x51, 0xa7, 0x1c, 0x8e, 0x7a, 0x98, 0x3c, 0xeb, 0xac, 0x54, 0x84, 0xf7, 0x62, 0x88, 
		0x64, 0xa8, 0xbb, 0xab, 0xe1, 0x95, 0x94, 0x41, 0x2a, 0x60, 0x30, 0xcc, 0x48, 0xd2, 0x89, 0xb2, 
		0x65, 0x76, 0x0a, 0xb8, 0x56, 0x4f, 0xc3, 0x87, 0xdd, 0x4c, 0xc2, 0xd4, 0x82, 0x35, 0x90, 0xa2, 
		0x5f, 0xad, 0x19, 0x74, 0x73, 0xd0, 0x24, 0x69, 0x20, 0x07, 0xdc, 0x1b, 0x44, 0x58, 0xff, 0x5a, 
		0x6c, 0xf2, 0xfb, 0x8c, 0x79, 0x97, 0xa6, 0x22, 0xb4, 0x7e, 0x5b, 0x17, 0x2f, 0x91, 0x71, 0xfe, 
		0x38, 0xa3, 0x05, 0xb1, 0xba, 0x99, 0xd9, 0xf1, 0x21, 0x5c, 0x67, 0x6d, 0xde, 0xaa, 0xc7, 0x8f, 
		0x81, 0x0b, 0xb0, 0xbc, 0x0c, 0xcd, 0x63, 0xc1, 0xfc, 0xc0, 0x42, 0x78, 0xc5, 0x8a, 0x06, 0x3d, 
		0x2e, 0x9e, 0xa1, 0x80, 0xb3, 0xf8, 0xe9, 0x68, 0xd1, 0x36, 0x70, 0x49, 0xc4, 0xd7, 0x2c, 0x6e, 
		0xe7, 0xb5, 0xbe, 0x92, 0xce, 0xed, 0xf3, 0x9c, 0xe4, 0x3b, 0x47, 0x2b, 0x85, 0x5d, 0x72, 0x01
		]

def padding(msg):
	if len(msg) % 32 != 0:
		extra = '*' * (32 - len(msg) % 32)
		return msg + extra
	else:
		return msg

def keygen(u, v):
	return [a ^ b for a, b in zip(u, v)][:20]

def roadrunner(table, roadrunner_wile, lili, lilibeth, omega):
	for z in range(16):
		roadrunner_wile[z] = (((omega[table[lili[z][0]]] | omega[table[lili[z][1]]]) +
			(omega[table[lili[z][2]]] | omega[table[lili[z][3]]])) ^ ((omega[table[lili[z][4]]] +
			omega[table[lili[z][5]]]) + (omega[table[lili[z][6]]] ^ omega[table[lili[z][7]]]))) % 256
		roadrunner_wile[z] = (roadrunner_wile[z] + (((~omega[table[lili[z][8]]] ^ omega[table[lili[z][9]]]) +
			(omega[table[lili[z][10]]] & ~omega[table[lili[z][11]]])) ^ ((omega[table[lili[z][12]]] ^ 
			~omega[table[lili[z][13]]]) + (omega[table[lili[z][14]]] ^ omega[table[lili[z][15]]])))) % 256
		roadrunner_wile[z] = (roadrunner_wile[z] + lilibeth[roadrunner_wile[z]] + lilibeth[z]) % 256
	return roadrunner_wile

def roadrunner_init(table, roadrunner_wile, lili, lilibeth, omega):
	SBOX = [
		[10, 11, 4, 5, 15, 0, 2, 3, 1, 9, 14, 6, 7, 12, 8, 13], 
		[1, 11, 13, 2, 0, 7, 3, 8, 14, 4, 6, 15, 5, 10, 12, 9], 
		[1, 9, 0, 4, 11, 5, 2, 8, 15, 7, 3, 6, 10, 14, 13, 12], 
		[5, 0, 9, 8, 3, 10, 12, 4, 1, 6, 7, 11, 15, 14, 2, 13], 
		[10, 6, 13, 3, 2, 11, 12, 14, 5, 9, 4, 1, 0, 8, 15, 7], 
		[15, 6, 1, 10, 7, 13, 14, 8, 3, 12, 0, 5, 2, 9, 4, 11], 
		[13, 7, 9, 5, 14, 12, 8, 15, 6, 0, 10, 4, 3, 11, 2, 1], 
		[13, 15, 8, 10, 6, 11, 9, 7, 12, 2, 3, 4, 14, 0, 5, 1], 
		[11, 3, 14, 7, 4, 8, 12, 2, 13, 0, 6, 1, 9, 10, 5, 15], 
		[2, 3, 14, 9, 11, 5, 15, 0, 4, 7, 1, 6, 12, 13, 8, 10], 
		[13, 3, 14, 1, 10, 0, 6, 5, 7, 2, 4, 9, 12, 8, 11, 15], 
		[15, 7, 4, 12, 14, 2, 9, 6, 3, 1, 13, 5, 0, 8, 11, 10], 
		[10, 7, 5, 14, 6, 2, 15, 1, 8, 11, 12, 9, 0, 3, 4, 13], 
		[1, 5, 0, 4, 6, 9, 11, 12, 3, 14, 7, 2, 15, 8, 13, 10], 
		[14, 9, 11, 2, 10, 4, 3, 0, 5, 8, 6, 15, 1, 12, 13, 7], 
		[11, 13, 6, 2, 0, 9, 3, 12, 1, 8, 7, 15, 4, 5, 10, 14]
		]
	for z in range(16):
		roadrunner_wile[z] = (((omega[table[SBOX[z][0]]] | omega[table[SBOX[z][1]]]) +
			(omega[table[SBOX[z][2]]] | omega[table[SBOX[z][3]]])) ^ ((omega[table[SBOX[z][4]]] +
			omega[table[SBOX[z][5]]]) + ( omega[table[SBOX[z][6]]] ^ omega[table[SBOX[z][7]]]))) % 256
		roadrunner_wile[z] = (roadrunner_wile[z] + (((~omega[table[SBOX[z][8]]] ^ omega[table[SBOX[z][9]]]) + 
			(omega[table[SBOX[z][10]]] & ~omega[table[SBOX[z][11]]])) ^ ((omega[table[SBOX[z][12]]] ^ 
			~omega[table[SBOX[z][13]]]) + (omega[table[SBOX[z][14]]] ^ omega[table[SBOX[z][15]]])))) % 256
	return roadrunner_wile

def circle_it_out(msg, ruler, roadrunner_wile, lili, lilibeth, enc, l, r, omega):
	for i in range(16):
		l[0][i] = msg[i]
		r[0][i] = msg[i+16]
	for i in range(1, ruler):
		roadrunner_wile = roadrunner(r[i-1], roadrunner_wile, lili, lilibeth, omega)
		for y in range(16):
			l[i][y] = r[i-1][y]
			r[i][y] = (l[i-1][y] ^ roadrunner_wile[y])%256
	for i in range(16):
		enc[i+16] = l[ruler-1][i]%256
		enc[i] = r[ruler-1][i]%256
	return roadrunner_wile, enc, l, r

def circle_it_out_init(msg, ruler, roadrunner_wile, lili, lilibeth, enc, l, r, omega):
	for i in range(16):
		l[0][i] = msg[i]
		r[0][i] = msg[i+16]
	for i in range(1,ruler):
		roadrunner_wile = roadrunner_init(r[i-1], roadrunner_wile, lili, lilibeth, omega)
		for y in range(16):
			l[i][y] = r[i-1][y]
			r[i][y] = (l[i-1][y] ^ roadrunner_wile[y])%256
	for i in range(16):
		enc[i] = l[ruler-1][i]%256
		enc[i+16] = r[ruler-1][i]%256
	return roadrunner_wile, enc, l, r

def persian_init(key, roadrunner_wile, lili, lilibeth, enc, l, r, omega, Omega):
	stkey = [88, 20, 64, 181, 251, 167, 69, 243, 205, 166, 110, 65, 90, 176, 229, 46, 206, 104, 15, 19, 49, 101, 3, 223, 221, 231, 232, 43, 62, 193, 80, 228]
	for compt in range(256):
		omega[compt] = (Omega[compt]^key[compt%20]) % 256
	for w in range(4):
		roadrunner_wile, enc, l, r = circle_it_out_init(stkey, 32, roadrunner_wile, lili, lilibeth, enc, l, r, omega);
		for compt in range(256):
			omega[compt] = (omega[compt]^enc[compt%32])%256
		for compt in range(32):
			stkey[compt] = enc[compt]
	for compt in range(16):
		err = 0
		ix = 0
		while ix < 16:
			roadrunner_wile, enc, l, r = circle_it_out_init(enc, 4, roadrunner_wile, lili, lilibeth, enc, l, r, omega)
			x = 0
			while x < ix:
				if lili[compt][x] == (enc[7]%16):
					x = ix
					err = 1
					roadrunner_wile, enc, l, r = circle_it_out_init(enc, 4, roadrunner_wile, lili, lilibeth, enc, l, r, omega)
				else: x += 1
			if err == 0: lili[compt][ix] = enc[7]%16
			else:
				err = 0;
				ix = ix-1;
			ix += 1
	err = 0 
	ix = 0
	while ix < 256:
		roadrunner_wile, enc, l, r = circle_it_out_init(enc, 4, roadrunner_wile, lili, lilibeth, enc, l, r, omega)
		x = 0
		while x < ix:
			if lilibeth[x] == ( enc[7]%256):
				x  = ix 
				err = 1
				roadrunner_wile, enc, l, r = circle_it_out_init(enc, 4, roadrunner_wile, lili, lilibeth, enc, l, r, omega)
			else:	
				x += 1
		if err == 0: lilibeth[ix]=enc[7]%256
		else:
			err = 0;
			ix = ix-1;
		ix += 1
	for compt in range(256):
		omega[compt] = (omega[compt] ^ key[compt%20])%256	
	for w in range(4):
		roadrunner_wile, enc, l, r = circle_it_out_init(stkey, 32, roadrunner_wile, lili, lilibeth, enc, l, r, omega)
		for compt in range(256):
			omega[compt] = (omega[compt] ^ enc[compt%32])%256
		for compt in range(32):
			stkey[compt] = enc[compt]
	return roadrunner_wile, lili, lilibeth, enc, l, r, omega

def encrypt_iginition(msg, key):
	roadrunner_wile = [0 for x in range(16)]
	lili = [[0 for x in range(16)] for y in range(256)] 
	lilibeth, omega = [[0 for x in range(256)] for _ in '01']
	enc = [0 for x in range(32)]
	l, r = [[[0 for x in range(16)] for y in range(32)] for _ in '01'] 
	roadrunner_wile, lili, lilibeth, enc, l, r, omega = persian_init(key, roadrunner_wile, lili, lilibeth, enc, l, r, omega, Omega)
	roadrunner_wile, enc, l, r = circle_it_out(msg, 6, roadrunner_wile, lili, lilibeth, enc, l, r, omega)
	return enc

def encrypt(msg, key):
	msg = padding(msg)
	blocks = [msg[i*32:i*32+32] for i in range(len(msg) // 32)]
	ciphers = []
	enc = encrypt_iginition([ord(item) for item in blocks[0]], key)
	ciphers.append(enc)
	for i in range(len(blocks)-1):
		enc = encrypt_iginition([ord(item) for item in blocks[i+1]], keygen([ord(item) for item in blocks[i]], ciphers[i]))
		ciphers.append(enc)
	return "".join("".join(str(format(i, "02x")) for i in item) for item in ciphers)

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

def main():
	border = "|"
	pr(border*72)
	pr(border, "Hello guys! This challenge is about breaking a symmetric cipher that", border)
	pr(border, "we have implemented here, your mission is find the flag, have fun :)", border)
	pr(border*72)

	while True:
		pr("| Options: \n|\t[E]encrypt message \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'e':
			pr(border, 'please send you message: ')
			msg = sc()
			enc = encrypt(msg + flag, skey)
			pr(border, f'enc = {enc}')
		elif ans == 'q': die("Quitting ...")
		else: die("Bye bye ...")

if __name__ == '__main__':
	main()