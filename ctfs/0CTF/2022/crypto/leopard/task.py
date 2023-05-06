#!/usr/bin/env python3

import random
import signal
import socketserver
import string
from cipher import AEAD
from hashlib import sha256
from os import urandom
from secret import flag

class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def proof_of_work(self):
        random.seed(urandom(8))
        proof = ''.join([random.choice(string.ascii_letters + string.digits + '!#$%&*-?') for _ in range(20)])
        digest = sha256(proof.encode()).hexdigest()
        self.dosend('sha256(XXXX + {}) == {}'.format(proof[4: ], digest))
        self.dosend('Give me XXXX:')
        x = self.request.recv(10)
        x = (x.strip()).decode('utf-8') 
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

    def handle(self):
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(50)
            if not self.proof_of_work():
                self.dosend('You must pass the PoW!')
                return
            signal.alarm(300)
            msg = b'The quick brown fox jumps over the lazy dog.'
            ad = b'0CTF2022'
            key = urandom(16)
            iv = urandom(16)
            C1 = AEAD(key, iv)
            C2 = AEAD(key, iv, True)
            ct1, _ = C1.encrypt(msg, ad)
            ct2, _ = C2.encrypt(msg, ad)
            self.dosend(ct1.hex())
            self.dosend(ct2.hex())
            key_ = self.request.recv(64).strip()
            iv_ = self.request.recv(64).strip()
            if key.hex().encode('latin-1') == key_ and iv.hex().encode('latin-1') == iv_:
                self.dosend(flag)
            else:
                self.dosend(':(')
        except TimeoutError:
            self.dosend('Timeout!')
            self.request.close()
        except:
            self.dosend('Wtf?')
            self.request.close()

class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 31337
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
