import binascii
import socketserver

from Crypto.Random.random import choice
from Crypto.Util.asn1 import DerSequence

import benaloh

answers = [
		b'It is certain',
		b'It is decidedly so',
		b'Without a doubt',
		b'Yes definitely',
		b'You may rely on it',
		b'As I see it, yes',
		b'Most likely',
		b'Outlook good',
		b'Yes',
		b'Signs point to yes',
		b'Reply hazy try again',
		b'Ask again later',
		b'Better not tell you now',
		b'Cannot predict now',
		b'Concentrate and ask again',
		b'Don\'t count on it',
		b'My reply is no',
		b'My sources say no',
		b'Outlook not so good',
		b'Very doubtful'
	]

sk = benaloh.unpack('sk')

def handle(self):
	while True:
		der = DerSequence()
		der.decode(binascii.unhexlify(self.query(b'Question: ')))
		question = bytes([benaloh.decrypt(c, sk) for c in der])
		response = choice(answers)
		self.write(response)

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