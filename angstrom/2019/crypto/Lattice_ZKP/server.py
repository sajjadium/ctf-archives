import binascii
import numpy as np
import socketserver

from Crypto.Util.asn1 import DerSequence

import lwe

welcome = rb'''
    __      __  __  _                    __       
   / /___ _/ /_/ /_(_)_______     ____  / /______ 
  / / __ `/ __/ __/ / ___/ _ \   /_  / / //_/ __ \
 / / /_/ / /_/ /_/ / /__/  __/    / /_/ ,< / /_/ /
/_/\__,_/\__/\__/_/\___/\___/    /___/_/|_/ .___/ 
                                         /_/      
Query until you are convinced that I know s, where
b = A*s + e
'''

choices = b'''\
[0] r
[1] r+s'''

with open('A.npy', 'rb') as f:
	A = np.load(f)

with open('s.npy', 'rb') as f:
	s = np.load(f)

pack = lambda x: binascii.hexlify(DerSequence(x.tolist()).encode())

def handle(self):
	self.write(welcome)
	r, b = lwe.sample(A)
	self.write(b'A*r + e: %b' % pack(b))
	self.write(choices)
	choice = self.query(b'Choice: ')
	if choice == b'0':
		self.write(b'r: %b' % pack(r))
	elif choice == b'1':
		self.write(b'r+s: %b' % pack(lwe.add(r, s)))
	else:
		self.write(b'Invalid choice.')

class RequestHandler(socketserver.BaseRequestHandler):

	handle = handle

	def read(self, until=b'\n'):
		out = b''
		while not out.endswith(until):
			out += self.request.recv(1)
		return out[:-len(until)]

	def query(self, string=b''):
		self.write(string, newline=False)
		return self.read()

	def write(self, string, newline=True):
		self.request.sendall(string)
		if newline:
			self.request.sendall(b'\n')

class Server(socketserver.ForkingTCPServer):

	allow_reuse_address = True

	def handle_error(self, request, client_address):
		pass

port = 3000
server = Server(('0.0.0.0', port), RequestHandler)
server.serve_forever()