#!/usr/bin/env python3
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256
import os


bits = 256
bs = AES.block_size
FLAG = open('flag.txt').read()

menu = """
+-------------------------+
|                         |
|        M E N U          |   
|                         |
| [1] DH Parameters       |
| [2] View PublicKeys     |
| [3] Encrypt Flag        |
| [4] Generate PublicKey  |
|                         |
+-------------------------+
"""

def encrypt(m, key):
	key = SHA256.new(str(key).encode()).digest()[:bs]
	iv = os.urandom(bs)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	enc = cipher.encrypt(pad(m.encode(), 16))
	return (enc.hex(), iv.hex())

def gen_pubkey(g, p, privkey):
	l = privkey.bit_length()
	m = int(input("Enter some random integer > "))
	new_privkey = privkey ^ m
	new_pubkey = pow(g, new_privkey, p)
	return new_pubkey

if __name__ == '__main__':
	g = 2
	p = getPrime(bits)

	# Rick Astley
	a = getRandomRange(1, p-1)
	R = pow(g,a,p)

	# Kermit the Frog
	b = getRandomRange(1, p-1)
	K = pow(g,b,p)

	s = pow(R,b,p)
	enc_flag, iv = encrypt(FLAG, s)

	# test
	with open('priv.txt','w') as f:
		f.write('a='+str(a)+'\n')
		f.write('b='+str(b))

	print(menu)
	l = p.bit_length() + 4
	
	try:
		for _ in range(l):
			ch = input("Choice ? ").strip().lower()

			if ch == '1':
				print("[DH parameters]")
				print(f"{g = }")
				print(f"{p = }\n")
			
			elif ch == '2':
				print("[Rick's PublicKey]")
				print(f"{R = }\n")
				print("[Kermit's PublicKey]")
				print(f"{K = }\n")
			
			elif ch == '3':
				print("[ENC FLAG]")
				print(f"{enc_flag = }\n")
				print("[IV]")
				print(f"{iv = }\n")

			elif ch == '4':
				npk = gen_pubkey(g, p, b)
				print("[Kermit's New PublicKey]")
				print(f"{npk = }\n")
			else:
				print(f":( Invalid Choice !!!")
				break
	except Exception as e:
		print(e)
		exit()
