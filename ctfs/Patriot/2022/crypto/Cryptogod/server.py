import sys
import socketserver
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

FLAG = "real_flag_is_defined_here"
KEY = get_random_bytes(16)
BS = AES.block_size
IV = b'\x00' * BS


def encrypt(username):
    if not isinstance(username, bytes): 
        username = username.encode()

    pt = pad(username, BS)
    tag = AES.new(KEY, AES.MODE_CBC, iv=IV).encrypt(pt)
    if len(tag) > 16:
        tag = tag[-16:]
    return tag.hex()


def admit_new_cryptogod(username):
    cryptogods.append(username)
    

MASTER_KEY = encrypt("cryptogodadministrator")
cryptogods = ["cryptogodadministrator"]


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        req = self.request
        stop = False

        req.sendall(b'To be accepted into the sect of the crypto gods, give us a username that will encrypt to ' + MASTER_KEY.encode() + b'\n~> ')
        username = req.recv(256)
        try:
            username = username.decode('ascii')
            if username in cryptogods:
                req.sendall(b'\n' + b'-' * 48 + b'\n\n')
                req.sendall(b"That username already belongs to a crypto god!\n")
                stop = True
        except:
            pass
        finally:
            if not stop:
                if encrypt(username) != MASTER_KEY:
                    req.sendall(b'\n' + b'-' * 48 + b'\n\n')
                    req.sendall(b"You are not a crypto god it seems...\n")
                else:
                    admit_new_cryptogod(username)
                    req.sendall(b'\n' + b'-' * 48 + b'\n\n')
                    req.sendall(FLAG.encode() + b"\n")
            else:
                pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    host, port = 'chal2.pctf.competitivecyber.club', 10001

    sys.stderr.write('Listening {}:{}\n'.format(host, port))
    server = ThreadedTCPServer((host, port), RequestHandler)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    server.serve_forever()