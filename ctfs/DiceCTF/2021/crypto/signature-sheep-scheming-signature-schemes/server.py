import signal
import socketserver
from lwe import Key, n

with open('public.key', 'rb') as f:
	key = Key.deserialize(f.read())

with open('flag.txt', 'rb') as f:
	flag = f.read()

message = b'shep, the conqueror'

class RequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		signal.alarm(10)
		self.request.sendall(b'signature? ')
		signature = self.request.recv(4*n)
		key.verify(message, signature)
		self.request.sendall(flag)

class Server(socketserver.ForkingTCPServer):

	allow_reuse_address = True

	def handle_error(self, request, client_address):
		self.request.close()

server = Server(('0.0.0.0', 3000), RequestHandler)
server.serve_forever()
