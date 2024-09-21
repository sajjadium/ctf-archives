#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from external import *
import socketserver, signal, json, os, re, sys
from io import StringIO

listen = 1337
attempts = 10000
flag = getflag()

guest = b"{'username':'guest_user','role':0}"

def encrypt(key,iv,message):
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return cipher.encrypt(pad(message,16)).hex()

def ispadding(dec):
	pad_b = dec[-2:]
	pad_amt = int("0x"+pad_b,16)
	valid = pad_b*pad_amt
	padding = dec[len(dec)-(pad_amt*2):]
	return valid==padding

def decrypt(key,token):
	iv = bytes.fromhex(token[:32].decode())
	ct = bytes.fromhex(token[32:].decode())
	cipher = AES.new(key, AES.MODE_CBC, iv)
	dec = cipher.decrypt(ct)
	return dec

def admin(tries,req):

	key = os.urandom(16)
	iv = os.urandom(16)
	eg = iv.hex()+encrypt(key,iv,b"print(1337)")

	req.sendall(b"====================================================================================================\n")
	req.sendall(b"||					ADMIN CONSOLE						||\n")
	req.sendall(b"||				RUN ENCRYPTED PYTHON CODE HERE					||\n")
	req.sendall(b"====================================================================================================\n")
	req.sendall(b" Example: "+str.encode(str(eg))+b"\n")
	while tries < attempts:
		req.sendall(b'Code ('+str.encode(str(tries))+b'/'+str.encode(str(attempts))+b'): ')
		c = req.recv(4096).strip(b'\n')
		try:
			code = decrypt(key,c)
			if ispadding(code.hex()):
				code = unpad(code,16)
				if re.match(b"print\([0-9a-zA-Z]*\)",code) != None:
					old_stdout = sys.stdout
					sys.stdout = mystdout = StringIO()
					try:
						eval(code)
					except Exception as e:
						print(str(e))
					sys.stdout = old_stdout
					req.sendall(mystdout.getvalue().encode())
					exit()
		except:
			pass
		tries += 1

def serve(req):
	tries = 0
	req.sendall(b"====================================================================================================\n")
	req.sendall(b"||                                           SECRET LOGIN                                         ||\n")
	req.sendall(b"||                                     AUTHORIZED PERSONNEL ONLY                                  ||\n")
	req.sendall(b"||                                                                                                ||\n")
	req.sendall(b"||                                    PROVIDE SECURE ACCESS TOKEN                                 ||\n")
	req.sendall(b"||                                                                                                ||\n")
	req.sendall(b"====================================================================================================\n")

	key = os.urandom(16)
	iv = os.urandom(16)
	guest_enc = iv.hex()+encrypt(key,iv,guest)

	req.sendall(b"Guest: "+str.encode(str(guest_enc))+b"\n")
	while tries < attempts:
		req.sendall(b'Access token ('+str.encode(str(tries))+b'/'+str.encode(str(attempts))+b'): ')
		t = req.recv(4096).strip(b'\n')
		try:
			token = decrypt(key,t)
			if ispadding(token.hex()):
				token = unpad(token,16)
			else:
				req.sendall(b"Error!\n")
		except Exception as e:
			print(str(e))
			tries += 1
			continue
		try:
			data = json.loads(token)
			if data['username'] == 'administrative_user' and data['role'] == 1:
				admin(tries,req)
		except:
			pass
		tries += 1

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
