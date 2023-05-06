from Crypto.Cipher import AES
from hashlib import md5
import hmac
from os import urandom
import sys
import random
from binascii import hexlify, unhexlify
import secret
import socket
import threading
import socketserver
import signal

host, port = '0.0.0.0', 5000
BUFF_SIZE = 1024

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	allow_reuse_address = True
class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):

	def handle(self):
		self.AES_BLOCK_SIZE = 32
		self.SIG_SIZE = md5().digest_size
		self.message = b'guest'
		self.key = self._hash_key(secret.key)
		self.enc_role, self.sig = self.encrypt(self.message)

		try:
			while True:
				self.menu()

				try:
					self.request.sendall(b'Your choice: ')
					opt = int(self.rfile.readline().decode())
				except ValueError:
					self.request.sendall(
						b'Invalid option!!!\n')
					continue
				if opt == 1:
					self.request.sendall(b'Data format: name=player101&role=enc_role&sign=sig, enc_role and sign are in hex.\n')
					self.request.sendall(b'Your data: ')
					data = self.rfile.readline().strip()
					self.confirm(data)
				elif opt == 2:
					self.request.sendall(b'Your data: ')
					data = self.rfile.readline().strip()
					if b'&role=' in data:
						self.request.sendall(b'Not that easy!\n')
					else:
						sign = self.sign_new(data)
						if sign == None:
							pass
						else:
							self.request.sendall(b"Hash: " + hexlify(sign) + b'\n')
				elif opt == 3:
					self.request.sendall(b'Your data: ')
					data = self.rfile.readline().strip()
					sign = self.sign_old(data)
					self.request.sendall(b"Hash: " + hexlify(sign) + b'\n')
				elif opt == 4:
					self.request.sendall(b'Goodbye!\n')
					return
				else:
					self.request.sendall(b'Invalid option!!!\n')

		except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
			print("{} disconnected".format(self.client_address[0]))

	def menu(self):
		self.request.sendall(b'\nYour role: ' + self.decrypt(b'name=player101&role='+hexlify(self.enc_role), hexlify(self.sig)))
		self.request.sendall(b'\nEncrypted data of your role:')
		self.request.sendall(b'\nEncrypted: ' + hexlify(self.enc_role))
		self.request.sendall(b'\nSignature: ' + hexlify(self.sig) + b'\n')
		self.request.sendall(b'1. Verify your data:\n')
		self.request.sendall(b'2. Sign your data in new way:\n')
		self.request.sendall(b'3. Sign your data in old way:\n')
		self.request.sendall(b'4. Quit\n')

	def _hash_key(self, key):
		return md5(key).digest()
	
	def _initialisation_vector(self):
		return urandom(16)
	
	def _cipher(self, key, iv):
		return AES.new(key, AES.MODE_CBC, iv)

	def encrypt(self, data):
		iv = self._initialisation_vector()
		cipher = self._cipher(self.key, iv)
		pad = self.AES_BLOCK_SIZE - len(data) % self.AES_BLOCK_SIZE
		data = data + (pad * chr(pad)).encode()
		data = iv + cipher.encrypt(data)
		ss = b'name=player101&role=%s'%(hexlify(data))
		sig = self.sign_new(ss)
		return data, sig
		
	def decrypt(self, data, sig):
		if hexlify(self.sign_new(data)) != sig:
			self.request.sendall(b'Message authentication failed')
			return
		else:
			pos = data.rfind(b'&role=')
			data = unhexlify(data[pos+6:])
			iv = data[:16]
			data = data[16:]
			cipher = AES.new(self.key, AES.MODE_CBC, iv)
			data = cipher.decrypt(data)
			return data[:-data[-1]]

	def XR(self, a, b):
		len_max = len(a) if len(a) > len(b) else len(b)
		s = ''
		for i in range(len_max):
			h = hex(a[i%len(a)] ^ b[i%len(b)])[2:]
			if(len(h) < 2):
				s += '0' + hex(a[i%len(a)] ^ b[i%len(b)])[2:]
			else:
				s += hex(a[i%len(a)] ^ b[i%len(b)])[2:]
		return unhexlify(s.encode())

	def xor_key(self, a):
		if isinstance(a, str):
			a = a.encode()
		b = self.key
		s = b''
		if len(a) > len(b):
			s += self.XR(a[:len(b)], b) + a[len(b):]
		elif len(a) < len(b):
			s += self.XR(b[:len(a)], a) + b[len(a):]
		return s

	def sign_old(self, data):
		return md5(self.xor_key(data)).digest()

	def sign_new(self, data):
		return hmac.new(self.key, data, md5).digest()

	def confirm(self, data):
		if isinstance(data, str):
			data = data.encode('utf-8')
		pos_name = data.rfind(b'name=')
		pos_role = data.rfind(b'&role=')
		pos_sign = data.rfind(b'&sign=')
		if pos_role == -1 or pos_sign == -1 or pos_name == -1:
			self.request.sendall(b'\nInvalid data!\n')
			return
		enc_role = data[:pos_sign]
		sign = data[pos_sign + 6:]
		try:
			check = self.decrypt(enc_role, sign)
		except Exception:
			self.request.sendall(b'\nInvalid data!\n')
		if check == b'royal':
			self.request.sendall(b'\nFlag here: ' + secret.flag)
		elif check == b'guest':
			self.request.sendall(b'\nHello peasant!\n')
		elif check == None:
			self.request.sendall(b'\nYou\'re a intruder!!!\n')
		else:
			self.request.sendall(b'\nStranger!!!\n')

	def parse_qsl(self, query):
		m = {}
		parts = query.split(b'&')
		for part in parts:
			key, val = part.split(b'=')
			m[key] = val
		return m


def main():
	server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print("Server loop running in thread:", server_thread.name)
	server_thread.join()

if __name__=='__main__':
	main()
