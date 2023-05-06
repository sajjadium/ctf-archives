#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def Eval_Poly(feedabck , States):
	next_s = 0
	for i in range(len(feedabck) - 1):
		if feedabck[i]:
			next_s = next_s + States[i]
	return next_s


flag = flag.lstrip('CCTF{').rstrip('}')
m = bytes_to_long(flag.encode('utf-8'))
IS, l = '0' + bin(m)[2:], len(bin(m)[2:]) + 1

registers= ['s' + str(i) for i in range(l)]
A = BooleanPolynomialRing(names = registers, order = TermOrder("lex"))

P = PolynomialRing(ZZ, 'x')
x, FF = P.gen(), GF(2)

IS = [FF(_) for _ in IS]
f = x^64 + x^33 + x^30 + x^26 + x^25 + x^24 + x^23 + x^22 + x^21 + x^20 + x^18 + x^13 + x^12 + x^11 + x^10 + x^7 + x^5 + x^4 + x^2 + x + 1
LFSR = LFSRCryptosystem(FF)

Encryptor = LFSR((f,IS))

ins = Encryptor.initial_state()
poly = [FF(_) for _ in f.list()]
SIZE = 2 ** (l // 4)
IKEY = lfsr_sequence(poly, IS, SIZE)
KEY = ''
for i in range(SIZE - l):
	S = [FF(t) for t in IKEY[i:i + l]]
	KEY += str(
		S[0] + S[12] + S[62] + S[18] + S[36] + 
		S[2]*S[8] + 
		S[34]*S[20] +
		S[27]*S[60] +
		S[31]*S[34] +
		S[63]*S[48] +
		S[50]*S[15] +
		S[25]*S[49] +
		S[49]*S[7]  +
		S[13]*S[61]*S[10] +
		S[32]*S[37]*S[29] +
		S[9]*S[6]*S[42] +
		S[59]*S[26]*S[55] +
		S[42]*S[41]*S[29] +
		S[58]*S[24]*S[28]
		)

enc = long_to_bytes(int(KEY, 2))
f = open('flag.enc', 'wb')
f.write(enc)
f.close()