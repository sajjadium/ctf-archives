import sys
import socketserver
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY = get_random_bytes(16)
FLAG = "real_flag_is_defined_here"


def encrypt(username,req):
    cipher = AES.new(KEY, AES.MODE_ECB)
    message = f"{username}, here is your top secret access code for today: {FLAG}"
    pad = 16 - (len(message) % 16)
    plaintext = message + (chr(pad)*pad)
    return cipher.encrypt(plaintext.encode()).hex().encode()


def validate(req):
    req.sendall(b'Please input your username to verify your identity. \n~> ')
    username = req.recv(256).decode('ascii')
    if username.split("\n")[0] == "admin":
        enc_message = encrypt(username,req)
        req.sendall(b'\n' + b'-' * 64 + b'\n')
        req.sendall(b"Here is you encrypted message:\n\n")
        req.sendall(enc_message + b'\n')
        return True
    return False


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        result = validate(self.request)
        if result is False:
            self.request.sendall(b'Invalid username.\n')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    host, port = 'chal2.pctf.competitivecyber.club', 10000

    sys.stderr.write('Listening {}:{}\n'.format(host, port))
    server = ThreadedTCPServer((host, port), RequestHandler)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    server.serve_forever()