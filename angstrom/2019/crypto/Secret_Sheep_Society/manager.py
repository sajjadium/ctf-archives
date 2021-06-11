import base64
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Manager:

	BLOCK_SIZE = AES.block_size

	def __init__(self, key):
		self.key = key

	def pack(self, session):
		cipher = AES.new(self.key, AES.MODE_CBC)
		iv = cipher.iv
		dec = json.dumps(session).encode()
		enc = cipher.encrypt(pad(dec, self.BLOCK_SIZE))
		raw = iv + enc
		return base64.b64encode(raw)

	def unpack(self, token):
		raw = base64.b64decode(token)
		iv = raw[:self.BLOCK_SIZE]
		enc = raw[self.BLOCK_SIZE:]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		dec = unpad(cipher.decrypt(enc), self.BLOCK_SIZE)
		return json.loads(dec.decode())