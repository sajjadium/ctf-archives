import base64
import signal
import SocketServer

import aes
import gm

PORT = 3000

message = open('message').read()

with open('sk') as f:
	p = int(f.readline())
	q = int(f.readline())
	sk = (p, q)

class incoming(SocketServer.BaseRequestHandler):
	def handle(self):
		req = self.request

		def receive():
			buf = ''
			while not buf.endswith('\n'):
				buf += req.recv(1)
			return buf[:-1]

		signal.alarm(60)
		
		req.sendall('Welcome to the Goldwasser-Micali key exchange!\n')
		req.sendall('Please send us an encrypted 128 bit key for us to use.\n')
		req.sendall('Each encrypted bit should be sent line by line in integer format.\n')

		enckey = []
		for i in range(128):
			enckey.append(int(receive()))
		key = gm.decrypt(enckey, sk)
		encmessage = aes.encrypt(key, message)

		req.sendall(base64.b64encode(encmessage)+'\n')
		req.close()

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
	pass

SocketServer.TCPServer.allow_reuse_address = True
server = ReusableTCPServer(('0.0.0.0', PORT), incoming)

print 'Server listening on port %d' % PORT
server.serve_forever()