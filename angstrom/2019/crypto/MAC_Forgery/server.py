import binascii
import socketserver

from cbc_mac import CBC_MAC
from secret import flag, key

welcome = b'''\
If you provide a message (besides this one) with
a valid message authentication code, I will give
you the flag.'''

cbc_mac = CBC_MAC(key)

def handle(self):
	iv, t = cbc_mac.generate(welcome)
	self.write(welcome)
	self.write(b'MAC: %b' % binascii.hexlify(iv+t))
	
	m = binascii.unhexlify(self.query(b'Message: '))
	mac = binascii.unhexlify(self.query(b'MAC: '))
	assert len(mac) == 32
	iv = mac[:16]
	t = mac[16:]

	if m != welcome and cbc_mac.verify(m, iv, t):
		self.write(flag)

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