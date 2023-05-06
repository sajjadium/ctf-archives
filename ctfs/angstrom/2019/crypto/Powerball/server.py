import socketserver

from Crypto.Util.number import getRandomRange

from secret import flag

welcome = b'''\
************  ANGSTROMCTF POWERBALL  ************
Correctly guess all 6 ball values ranging from 0
to 4095 to win the jackpot! As a special deal,
we'll also let you secretly view a ball's value!
'''

with open('public.txt') as f:
	n = int(f.readline()[3:])
	e = int(f.readline()[3:])

with open('private.txt') as f:
	d = int(f.readline()[3:])

def handle(self):
	self.write(welcome)
	balls = [getRandomRange(0, 4096) for _ in range(6)]
	x = [getRandomRange(0, n) for _ in range(6)]
	self.write('x: {}\n'.format(x).encode())
	v = int(self.query(b'v: '))
	m = []
	for i in range(6):
		k = pow(v-x[i], d, n)
		m.append((balls[i]+k) % n)
	self.write('m: {}\n'.format(m).encode())
	guess = []
	for i in range(6):
		guess.append(int(self.query('Ball {}: '.format(i+1).encode())))
	if balls == guess:
		self.write(b'JACKPOT!!!')
		self.write(flag)
	else:
		self.write(b'Sorry, those were the wrong numbers.')

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