from Crypto.Cipher import AES
import sig_sage as sig # this is generated from sig.sage
import hashlib

class Chain:
	def __init__(self, seed):
		self.flag = b"csaw{[REDACTED]}"
		self.ecdsa = sig.ECDSA(seed)
		self.blocks = {0: [hashlib.sha1(self.flag).digest(), self.ecdsa.sign(self.flag)]}

	def commit(self, message, num):
		formatted = self.blocks[num-1][0] + message
		sig = self.ecdsa.sign(formatted)
		self.blocks[num] = [hashlib.sha256(message).digest(), sig]

	def view_messages(self):
		return self.blocks

	def verify_sig(self, r, s, message):
		t = self.ecdsa.verify(r, s, message)
		return t