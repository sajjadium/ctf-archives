#!/usr/bin/env python3

import random
import signal
import socketserver
import string
from Chimera import Chimera
from hashlib import sha256
from os import urandom
from secret import flag

assert len(flag) == 21

MENU = '''
Feistel + SPN = Chimera
1. Enc
2. Dec
3. Exit
'''

def to_base64(x):
    bs = []
    while x:
        bs.append(x % 64)
        x //= 64
    return bs

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

    def recv_fromhex(self, l):
        passwd = self.request.recv(l).strip()
        passwd = bytes.fromhex(passwd.decode('latin-1'))
        return passwd

    def handle(self):
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(50)
            if not self.proof_of_work():
                self.dosend('You must pass the PoW!')
                return
            signal.alarm(300)
            flag_ = to_base64(int(flag[5: -1].hex(), 16))
            self.dosend('flag idx:')
            fidx = int(self.request.recv(64).strip())
            self.dosend('key idx:')
            kidx = int(self.request.recv(64).strip())
            key = bytearray(urandom(16))
            key[kidx] = flag_[fidx] << 2
            chimera = Chimera(key, 4)
            self.dosend(MENU)
            for _ in range(256):
                self.dosend('> ')
                op = int(self.request.recv(3).strip())
                if op == 1:
                    self.dosend('Pt: ')
                    pt = self.recv_fromhex(0x404)
                    assert len(pt) % 16 == 0
                    ct = chimera.encrypt(pt)
                    self.dosend(ct.hex())
                elif op == 2:
                    self.dosend('Ct: ')
                    ct = self.recv_fromhex(0x404)
                    assert len(ct) % 16 == 0
                    pt = chimera.decrypt(ct)
                    self.dosend(pt.hex())
                else:
                    return
        except TimeoutError:
            self.dosend('Timeout!')
            self.request.close()
        except:
            self.dosend('Wtf?')
            self.request.close()

class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 16666
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
