#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
from hmac import compare_digest
from random import shuffle
import os

flag = os.environ.get("FLAG", "ptm{REDACTED}")

BLOCK_SIZE = 16
NUM_BITS = BLOCK_SIZE * 8
SBOX = (0xC, 0x5, 0x6, 0xB,	0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2)
BIT_PERM = tuple((idx * 7) % NUM_BITS for idx in range(NUM_BITS))

def _pad_pkcs7(data, block_size = BLOCK_SIZE):
	return data + bytes([(block_size - len(data)) % block_size]) * ((block_size - len(data)) % block_size)

def _xor_bytes(left, right):
	return bytes(a ^ b for a, b in zip(left, right))

def _unpad_pkcs7(data, block_size = BLOCK_SIZE):
	d = data[-1]
	assert d <= len(data)
	assert all([x==d for x in data[-d:]])
	return data[:-d]

def _perm(data):
	state = data
	for _ in range(10):
		sbox_out = bytearray(len(state))
		for idx, value in enumerate(state):
			sbox_out[idx] = (SBOX[value >> 4] << 4) | SBOX[value & 0x0F]
		bits = []
		for value in sbox_out:
			for shift in range(8):
				bits.append((value >> (7 - shift)) & 0x01)
		permuted_bits = [0] * NUM_BITS
		for idx, bit in enumerate(bits):
			permuted_bits[BIT_PERM[idx]] = bit
		state_out = bytearray(len(state))
		for idx in range(len(state)):
			byte = 0
			for shift in range(8):
				byte = (byte << 1) | permuted_bits[idx * 8 + shift]
			state_out[idx] = byte
		state = bytes(state_out)
	return state

def _prf(block_index, key, data):
	cipher = AES.new(key, AES.MODE_ECB)
	mask = cipher.encrypt(sha256(block_index.to_bytes(4, 'big', signed=True)).digest())
	result = _xor_bytes(data, mask[:BLOCK_SIZE])
	result = _perm(result)
	result = _xor_bytes(result, mask[-BLOCK_SIZE:])
	return result


def enc_msg(key, nonce, message):
	padded = _pad_pkcs7(message)
	blocks = [padded[i : i + BLOCK_SIZE] for i in range(0, len(padded), BLOCK_SIZE)]
	ciphertext_blocks = []
	for idx, block in enumerate(blocks):
		keystream = _prf(idx, key, nonce)
		ciphertext_blocks.append(_xor_bytes(block, keystream))
	return b"".join(ciphertext_blocks)


def enc_tag(key, nonce, additional_data, ciphertext):
	ad_padded = _pad_pkcs7(nonce + additional_data)
	ct_padded = _pad_pkcs7(ciphertext)
	ad_blocks = [ad_padded[i : i + BLOCK_SIZE] for i in range(0, len(ad_padded), BLOCK_SIZE)]
	ct_blocks = [ct_padded[i : i + BLOCK_SIZE] for i in range(0, len(ct_padded), BLOCK_SIZE)]
	tag = ad_blocks[0]
	for idx, block in enumerate(ad_blocks[1:], start=1):
		keystream = _prf(idx + 1337, key, block)
		tag = _xor_bytes(tag, keystream)
	for idx, block in enumerate(ct_blocks):
		keystream = _prf(idx + 31337, key, block)
		tag = _xor_bytes(tag, keystream)
	return _prf(-1, key, tag)


def encrypt(key, nonce, message, additional_data):
	ciphertext = enc_msg(key, nonce, message)
	tag = enc_tag(key, nonce, additional_data, ciphertext)
	return ciphertext, tag

def decrypt(key, nonce, ciphertext,	additional_data, tag):
	assert len(key) == BLOCK_SIZE
	assert len(nonce) == BLOCK_SIZE
	assert len(ciphertext) % BLOCK_SIZE == 0
	assert len(tag) == BLOCK_SIZE

	expected_tag = enc_tag(key, nonce, additional_data, ciphertext)
	if not compare_digest(expected_tag, tag):
		return False
	blocks = [ciphertext[i : i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
	plaintext_blocks = []
	for idx, block in enumerate(blocks):
		keystream = _prf(idx, key, nonce)
		plaintext_blocks.append(_xor_bytes(block, keystream))
	plaintext_padded = b"".join(plaintext_blocks)
	try:
		plaintext = _unpad_pkcs7(plaintext_padded)
	except:
		return b"Invalid padding"
	return plaintext

if __name__ == "__main__":
	for r in range(5):
		base = list("m0leCon")
		shuffle(base)
		key = bytes(sha256("".join(base).encode()).digest())[:BLOCK_SIZE]
		for _ in range(16):
			nonces = bytes.fromhex(input("Enter nonce (hex): ").strip())
			nonces = [nonces[i:i+BLOCK_SIZE] for i in range(0, len(nonces), BLOCK_SIZE)]
			additional_data = bytes.fromhex(input("Enter additional_data (hex): ").strip())
			ciphertext = bytes.fromhex(input("Enter ciphertext (hex): ").strip())
			tag = bytes.fromhex(input("Enter tag (hex): ").strip())
			decs = [decrypt(key, nonce, ciphertext, additional_data, tag) for nonce in nonces]
			auth = any(decs)
			if auth:
				if additional_data != b"pretty please":
					print("Can you at least say 'please' next time?")
					exit()
				else:
					if all([dec == b"next round please" for dec in decs]):
						print("There you go!")
						break
					else:
						print("This message does not seem ok :(")
			else:
				print("Tag is invalid")
		else:
			print("Better luck next time!")
			exit()

	print(flag)