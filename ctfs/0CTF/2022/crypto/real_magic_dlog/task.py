#!/usr/bin/env python3

import random
import signal
import socketserver
import string
from Crypto.Util.number import *
from hashlib import sha256, sha384
from os import urandom
from secret import flag

LEN = 17

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
            signal.alarm(60)
            magic = urandom(LEN)
            magic_num = bytes_to_long(magic)
            self.dosend(magic.hex())
            self.dosend('P:>')
            P = int(self.request.recv(100).strip(), 16)
            self.dosend('E:>')
            E = int(self.request.recv(100).strip(), 16)
            self.dosend('data:>')
            data = self.request.recv(100).strip()
            num1 = int(data, 16)
            if P >> (384 - LEN * 8) == magic_num and isPrime(P):
                data2 = sha384(data).hexdigest()
                num2 = int(data2, 16)
                if pow(num1, E, P) == num2 % P:
                    self.dosend(flag)
                else:
                    self.dosend('try harder!!!')
        except TimeoutError:
            self.dosend('Timeout!')
            self.request.close()
        except:
            self.dosend('Wtf?')
            self.request.close()

class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 15555
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()