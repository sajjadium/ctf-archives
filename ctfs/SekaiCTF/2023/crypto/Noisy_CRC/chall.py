import secrets
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256

from flag import FLAG

def getCRC16(msg, gen_poly):
	assert (1 << 16) <= gen_poly < (1 << 17)  # check if deg = 16
	msglen = msg.bit_length()

	msg <<= 16
	for i in range(msglen - 1, -1, -1):
		if (msg >> (i + 16)) & 1:
			msg ^= (gen_poly << i)

	return msg

def oracle(secret, gen_poly):
	res = [secrets.randbits(16) for _ in range(3)] 
	res[secrets.randbelow(3)] = getCRC16(secret, gen_poly)
	return res


def main():
	key = secrets.randbits(512)
	cipher = AES.new(sha256(long_to_bytes(key)).digest()[:16], AES.MODE_CTR, nonce=b"12345678")
	enc_flag = cipher.encrypt(FLAG)
	print(f"Encrypted flag: {enc_flag.hex()}")

	used = set({})

	while True:
		gen_poly = int(input("Give me your generator polynomial: "))
		assert (1 << 16) <= gen_poly < (1 << 17)  # check if deg = 16

		if gen_poly in used:
			print("No cheating")
			exit(1)

		used.add(gen_poly)

		print(oracle(key, gen_poly))

main()