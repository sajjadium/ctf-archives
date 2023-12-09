#!/usr/bin/env python3

import random
import signal
import socketserver
import string
from Cipher import BlockCipher
from hashlib import sha256
from os import urandom
from secret import FLAG

MENU = """
[1] Encrypt
[2] Decrypt
[3] Guess"""

def get_key():
    key = b''
    while len(key) < 9:
        b = urandom(1)
        if b[0] < 243:
            key += b
    return key

class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def proof_of_work(self):
        random.seed(urandom(16))
        proof = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        digest = sha256(proof.encode()).hexdigest()
        self.dosend('sha256(XXXX + {}) == {}'.format(proof[4: ], digest))
        self.dosend('Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip().decode('latin-1')
        if len(x) != 4 or sha256((x + proof[4: ]).encode()).hexdigest() != digest:
            return False
        return True

    def dosend(self, msg):
        try:
            self.request.sendall(msg.encode('latin-1') + b'\n')
        except:
            pass

    def timeout_handler(self, signum, frame):
        raise TimeoutError

    def recvn(self, sz):
        r = sz
        res = b''
        while r > 0:
            res += self.request.recv(r)
            if res.endswith(b'\n'):
                r = 0
            else:
                r = sz - len(res)
        res = res.strip()
        return res

    def handle(self):
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(60)
            if not self.proof_of_work():
                self.dosend('You must pass the PoW!')
                return

            signal.alarm(int(337.1))
            key = get_key()
            cipher = BlockCipher(key, 5)

            self.dosend(MENU)
            for _ in range(int(133.7)):
                op = int(self.recvn(2))
                if op == 1:
                    self.dosend('pt: ')
                    pt = bytes.fromhex(self.recvn(19).decode())
                    assert all(bb < 243 for bb in pt)
                    ct = cipher.encrypt(pt)
                    self.dosend('ct: ' + ct.hex())
                elif op == 2:
                    self.dosend('ct: ')
                    ct = bytes.fromhex(self.recvn(19).decode())
                    assert all(bb < 243 for bb in ct)
                    pt = cipher.decrypt(ct)
                    self.dosend('pt: ' + pt.hex())
                elif op == 3:
                    guess = bytes.fromhex(self.recvn(19).decode())
                    if guess == key:
                        self.dosend('Wow, how do you know that?')
                        self.dosend('Here is the flag: ' + FLAG)
                    else:
                        self.dosend('Wrong!')
                    break
                else:
                    break
        except TimeoutError:
            self.dosend('Timeout!')
        except:
            self.dosend('GG')
        self.request.close()

class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 31338
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()