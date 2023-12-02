from Crypto.Util.number import *
import os

def xor(a, b):
  return bytes(i^j for i, j in zip(a,b))

sbox = [239, 209, 87, 244, 56, 155, 29, 190, 230, 69, 8, 96, 172, 15, 137, 42, 
		52, 154, 28, 191, 115, 208, 86, 245, 173, 14, 136, 43, 231, 134, 194, 97, 
		228, 71, 193, 98, 174, 13, 139, 40, 112, 211, 85, 246, 58, 2, 31, 188, 
		175, 12, 138, 41, 229, 70, 192, 99, 59, 152, 30, 189, 113, 210, 84, 247, 
		61, 158, 24, 187, 119, 212, 82, 249, 169, 10, 140, 47, 227, 64, 198, 101, 
		118, 213, 83, 240, 60, 159, 25, 186, 226, 65, 199, 100, 168, 11, 141, 46, 
		171, 195, 142, 45, 225, 66, 196, 0, 63, 156, 26, 185, 117, 214, 80, 243, 
		224, 67, 197, 102, 170, 9, 143, 44, 116, 215, 81, 242, 62, 157, 27, 184, 
		236, 79, 201, 106, 166, 5, 131, 32, 120, 219, 93, 254, 50, 145, 23, 180, 
		167, 4, 130, 33, 75, 78, 200, 107, 51, 144, 22, 181, 121, 218, 92, 255, 
		122, 217, 95, 252, 48, 147, 21, 182, 238, 77, 203, 104, 164, 7, 129, 34, 
		49, 146, 20, 183, 123, 216, 94, 253, 165, 6, 128, 35, 114, 76, 202, 105, 
		163, 103, 68, 37, 233, 74, 204, 111, 55, 148, 18, 177, 125, 222, 88, 251, 
		232, 237, 205, 110, 162, 1, 135, 36, 124, 223, 89, 250, 54, 149, 19, 176, 
		53, 150, 16, 179, 127, 220, 90, 241, 161, 153, 132, 39, 235, 72, 206, 109, 
		126, 221, 91, 248, 57, 151, 17, 178, 234, 73, 207, 108, 160, 3, 133, 38]
		
permute = [10, 11, 5, 6, 2, 4, 8, 0, 12, 9, 3, 13, 14, 15, 1, 7]

BLOCK_LEN = 16

class SPN:
	def __init__(self, key, iv):
		self.master_key = key
		self.iv = iv
		self.round_keys = self.expand_key()

	def expand_key(self):
		round_keys = [self.master_key]
		for i in range(42):
			round_keys.append(round_keys[-1][2:] + round_keys[-1][:2])
		return round_keys

	def pad(self, plaintext):
		return plaintext + b"\x00"*(BLOCK_LEN - (len(plaintext) % BLOCK_LEN))

	def permute(self, block):
		permuted = b""
		for i in permute:
			permuted += block[i].to_bytes(1, 'little')
		return permuted

	def add_key(self, block, round_key):
		return xor(block, round_key)

	def substitute(self, block):
		subbed = b""
		for i in block:
			subbed += sbox[i].to_bytes(1, 'little')
		return subbed

	def encrypt_block(self, block):
		for i in range(42):
			block = self.add_key(block, self.round_keys[i])
			block = self.substitute(block)
			block = self.permute(block)
		block = self.add_key(block, self.round_keys[42])
		return block

	def encrypt(self, plaintext):
		padded = self.pad(plaintext)
		blocks = [padded[i:i+BLOCK_LEN] for i in range(0,len(padded),BLOCK_LEN)]

		ct = self.iv
		for i in range(len(blocks)):
			temp = self.encrypt_block(blocks[i])
			ct += xor(temp, ct[16*i:16*i+16])
		return ct

key = os.urandom(16)
iv = os.urandom(16)
spn = SPN(key, iv)

flag = b"nbctf{[REDACTED]}"
print("Encrypted flag: " + spn.encrypt(flag).hex())

for _ in range(len("01234567")):
	a,b = list(map(int, input("Pick 2 indexes to swap for values in SBOX (x,y): ").split(",")))
	sbox[a], sbox[b] = sbox[b], sbox[a]

plaintext = bytes.fromhex(input("I'll let you encrypt one block of plaintext(hex): "))
assert len(plaintext) == 16, "NO NO NO NO NO"

print("Ciphertext: " + spn.encrypt(plaintext).hex())
