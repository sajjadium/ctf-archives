#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from external import *
import socketserver, signal

listen = 1337
attempts = 1500
flag = getflag()

def encrypt(key,plaintext):
	cipher = AES.new(key, AES.MODE_ECB)
	pt = pad(plaintext + flag.encode(), 16)
	return cipher.encrypt(pt).hex()

def serve(req):
	key = get_random_bytes(16)
	tries = 0
	req.sendall(b"Thank you for using our secure communications channel.\nThis channel uses top-shelf military-grade encryption.\nIf you are not the intended recepient, you can't read our secret.")
	while tries < attempts:
		req.sendall(b'\n('+str.encode(str(tries))+b'/'+str.encode(str(attempts))+b') ')
		req.sendall(b'Send challenge > ')
		try:
			ct = encrypt(key, req.recv(4096).strip(b'\n'))
			req.sendall(b"Response > " + ct.encode() + b'\n')
		except Exception as e:
			req.sendall(b"An error occured!\n")
		tries += 1
	req.sendall(b'\nMax attempts exceeded, have a good day.\n')

class incoming(socketserver.BaseRequestHandler):
	def handle(self):
		signal.alarm(1500)
		req = self.request
		serve(req)

def main():
	socketserver.TCPServer.allow_reuse_address = True
	server = ReusableTCPServer(("0.0.0.0", listen), incoming)
	server.serve_forever()

if __name__ == "__main__":
	main()
