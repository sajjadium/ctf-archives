from Crypto.Util.number import *
import random
flag = open('flag.txt','rb').read()
pt = bytes_to_long(flag)
bits = 768
p,q = getPrime(bits),getPrime(bits)
n = p*q
e = 0x10001
print(pow(pt,e,n))
bit_p = bin(p)[2:]
bit_q = bin(q)[2:]
parts = [bit_p[0:bits//3],bit_p[bits//3:2*bits//3],bit_p[2*bits//3:bits],bit_q[0:bits//3],bit_q[bits//3:2*bits//3],bit_q[2*bits//3:bits]]
random.shuffle(parts)
print(parts)