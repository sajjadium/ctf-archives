#!/usr/local/bin/python

import ctypes
import os

from Crypto.Util.strxor import strxor
from Crypto.Hash import SHAKE128

PRIVATE_KEY_SIZE = 74
PUBLIC_KEY_SIZE = 64

# make libcsidh.so
libcsidh = ctypes.CDLL('./libcsidh.so')

def stream(buf, ss):
	pad = SHAKE128.new(bytes(ss)).read(len(buf))
	return strxor(buf, pad)

def keygen():
	priv = ctypes.create_string_buffer(PRIVATE_KEY_SIZE)
	pub = ctypes.create_string_buffer(PUBLIC_KEY_SIZE)
	libcsidh.csidh_private(priv)
	libcsidh.csidh(pub, libcsidh.base, priv)
	return priv, pub

def apply_iso(start, iso):
	end = ctypes.create_string_buffer(PUBLIC_KEY_SIZE)
	libcsidh.csidh(end, start, iso)
	return end

def invert(priv):
	exponents = [-e % 256 for e in bytes(priv)]
	return ctypes.create_string_buffer(bytes(exponents))

class Alice:
	def __init__(self, msg0, msg1):
		assert type(msg0) == bytes
		assert type(msg1) == bytes
		assert len(msg0) == len(msg1)
		self.msg0 = msg0
		self.msg1 = msg1
		self.priv0, self.pub0 = keygen()
		self.priv1, self.pub1 = keygen()

	def publish(self):
		return self.pub0, self.pub1

	def encrypt(self, mask):
		ss0 = apply_iso(mask, invert(self.priv0))
		ss1 = apply_iso(mask, invert(self.priv1))
		enc0 = stream(self.msg0, ss0)
		enc1 = stream(self.msg1, ss1)
		return enc0, enc1

class Bob:
	def __init__(self, bit):
		assert bit in (0, 1)
		self.bit = bit
		self.iso, self.ss = keygen()

	def query(self, pubs):
		pub = pubs[self.bit]
		mask = apply_iso(pub, self.iso)
		return mask

	def decrypt(self, encs):
		enc = encs[self.bit]
		msg = stream(enc, self.ss)
		return msg

if __name__ == '__main__':
	with open('flag.txt', 'rb') as f:
		flag = f.read().strip()

	msg0 = os.urandom(len(flag))
	msg1 = strxor(msg0, flag)

	alice = Alice(msg0, msg1)
	pub0, pub1 = alice.publish()
	print(f'pub0: {bytes(pub0).hex()}')
	print(f'pub1: {bytes(pub1).hex()}')

	'''
	bob = Bob(bit)
	mask = bob.query((pub0, pub1))
	'''

	mask_hex = input('mask: ')
	mask = ctypes.create_string_buffer(bytes.fromhex(mask_hex), PUBLIC_KEY_SIZE)
	enc0, enc1 = alice.encrypt(mask)
	print(f'enc0: {enc0.hex()}')
	print(f'enc1: {enc1.hex()}')

	'''
	msg = bob.decrypt((enc0, enc1))
	'''
