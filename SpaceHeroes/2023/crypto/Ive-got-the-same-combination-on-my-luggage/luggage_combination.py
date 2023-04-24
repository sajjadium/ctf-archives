from pwn import *

plaintext = b'****************************************'
key1 = b'****************************************'
key2 = b'****************************************'

def shield_combination(p, k1, k2):
	A = xor(p, k1, k2)
	B = xor(p, k1)
	C = xor(p, k2)
	return A + B + C

print(shield_combination(plaintext, key1, key2).hex())
