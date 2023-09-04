import secrets
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256

from flag import FLAG

isIrreducible = [True for i in range(1 << 17)]

def init():
	for f in range(2, 1 << 17):
		if isIrreducible[f]:
			ls = [0] # store all multiples of polynomial `f`
			cur_term = f
			while cur_term < (1 << 17):
				ls = ls + [x ^ cur_term for x in ls]
				cur_term <<= 1

			for g in ls[2:]:  # the first two terms are 0, f respectively
				isIrreducible[g] = False

def getCRC16(msg, gen_poly):
	assert (1 << 16) <= gen_poly < (1 << 17)  # check if deg = 16
	msglen = msg.bit_length()

	msg <<= 16
	for i in range(msglen - 1, -1, -1):
		if (msg >> (i + 16)) & 1:
			msg ^= (gen_poly << i)

	return msg

def oracle(secret, gen_poly):
	l = int(13.37)
	res = [secrets.randbits(16) for _ in range(l)] 
	res[secrets.randbelow(l)] = getCRC16(secret, gen_poly)
	return res


def main():
	init()  # build table of irreducible polynomials

	key = secrets.randbits(512)
	cipher = AES.new(sha256(long_to_bytes(key)).digest()[:16], AES.MODE_CTR, nonce=b"12345678")
	enc_flag = cipher.encrypt(FLAG)
	print(f"Encrypted flag: {enc_flag.hex()}")

	used = set({})

	for _ in range(int(133.7)):
		gen_poly = int(input("Give me your generator polynomial: "))
		assert (1 << 16) <= gen_poly < (1 << 17)  # check if deg = 16
		if not isIrreducible[gen_poly]:
			print("Invalid polynomial")
			exit(1)

		if gen_poly in used:
			print("No cheating")
			exit(1)

		used.add(gen_poly)

		print(oracle(key, gen_poly))

main()