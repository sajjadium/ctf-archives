#!/usr/bin/env python3

import random
import signal
import socketserver
import string
from hashlib import sha256
from os import urandom
from secret import flag

def _prod(L):
    p = 1
    for x in L:
        p *= x
    return p

def _sum(L):
    s = 0
    for x in L:
        s ^= x
    return s

def n2l(x, l):
    return list(map(int, '{{0:0{}b}}'.format(l).format(x)))

class Generator1:
    def __init__(self, key: list):
        assert len(key) == 64
        self.NFSR = key[: 48]
        self.LFSR = key[48: ]
        self.TAP = [0, 1, 12, 15]
        self.TAP2 = [[2], [5], [9], [15], [22], [26], [39], [26, 30], [5, 9], [15, 22, 26], [15, 22, 39], [9, 22, 26, 39]]
        self.h_IN = [2, 4, 7, 15, 27]
        self.h_OUT = [[1], [3], [0, 3], [0, 1, 2], [0, 2, 3], [0, 2, 4], [0, 1, 2, 4]]

    def g(self):
        x = self.NFSR
        return _sum(_prod(x[i] for i in j) for j in self.TAP2)

    def h(self):
        x = [self.LFSR[i] for i in self.h_IN[:-1]] + [self.NFSR[self.h_IN[-1]]]
        return _sum(_prod(x[i] for i in j) for j in self.h_OUT)

    def f(self):
        return _sum([self.NFSR[0], self.h()])

    def clock(self):
        o = self.f()
        self.NFSR = self.NFSR[1: ] + [self.LFSR[0] ^ self.g()]
        self.LFSR = self.LFSR[1: ] + [_sum(self.LFSR[i] for i in self.TAP)]
        return o

class Generator2:
    def __init__(self, key):
        assert len(key) == 64
        self.NFSR = key[: 16]
        self.LFSR = key[16: ]
        self.TAP = [0, 35]
        self.f_IN = [0, 10, 20, 30, 40, 47]
        self.f_OUT = [[0, 1, 2, 3], [0, 1, 2, 4, 5], [0, 1, 2, 5], [0, 1, 2], [0, 1, 3, 4, 5], [0, 1, 3, 5], [0, 1, 3], [0, 1, 4], [0, 1, 5], [0, 2, 3, 4, 5], [
            0, 2, 3], [0, 3, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 5], [1, 2], [1, 3, 5], [1, 3], [1, 4], [1], [2, 4, 5], [2, 4], [2], [3, 4], [4, 5], [4], [5]]
        self.TAP2 = [[0, 3, 7], [1, 11, 13, 15], [2, 9]]
        self.h_IN = [0, 2, 4, 6, 8, 13, 14]
        self.h_OUT = [[0, 1, 2, 3, 4, 5], [0, 1, 2, 4, 6], [1, 3, 4]]

    def f(self):
        x = [self.LFSR[i] for i in self.f_IN]
        return _sum(_prod(x[i] for i in j) for j in self.f_OUT)
 
    def h(self):
        x = [self.NFSR[i] for i in self.h_IN]
        return _sum(_prod(x[i] for i in j) for j in self.h_OUT)        

    def g(self):
        x = self.NFSR
        return _sum(_prod(x[i] for i in j) for j in self.TAP2)  

    def clock(self):
        self.LFSR = self.LFSR[1: ] + [_sum(self.LFSR[i] for i in self.TAP)]
        self.NFSR = self.NFSR[1: ] + [self.LFSR[1] ^ self.g()]
        return self.f() ^ self.h()

class Generator3:
    def __init__(self, key: list):
        assert len(key) == 64
        self.LFSR = key
        self.TAP = [0, 55]
        self.f_IN = [0, 8, 16, 24, 32, 40, 63]
        self.f_OUT = [[1], [6], [0, 1, 2, 3, 4, 5], [0, 1, 2, 4, 6]]

    def f(self):
        x = [self.LFSR[i] for i in self.f_IN]
        return _sum(_prod(x[i] for i in j) for j in self.f_OUT)

    def clock(self):
        self.LFSR = self.LFSR[1: ] + [_sum(self.LFSR[i] for i in self.TAP)]
        return self.f()

class zer0lfsr:
    def __init__(self, msk: int, t: int):
        if t == 1:
            self.g = Generator1(n2l(msk, 64))
        elif t == 2:
            self.g = Generator2(n2l(msk, 64))
        else:
            self.g = Generator3(n2l(msk, 64))
        self.t = t

    def next(self):
        for i in range(self.t):
            o = self.g.clock()
        return o

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
            signal.alarm(30)
            if not self.proof_of_work():
                self.dosend('You must pass the PoW!')
                return
            signal.alarm(50)
            available = [1, 2, 3]
            for _ in range(2):
                self.dosend('which one: ')
                idx = int(self.request.recv(10).strip())
                assert idx in available
                available.remove(idx)
                msk = random.getrandbits(64)
                lfsr = zer0lfsr(msk, idx)
                for i in range(5):
                    keystream = ''
                    for j in range(1000):
                        b = 0
                        for k in range(8):
                            b = (b << 1) + lfsr.next()
                        keystream += chr(b)
                    self.dosend('start:::' + keystream + ':::end')
                hint = sha256(str(msk).encode()).hexdigest()
                self.dosend('hint: ' + hint)
                self.dosend('k: ')
                guess = int(self.request.recv(100).strip())
                if guess != msk:
                    self.dosend('Wrong ;(')
                    self.request.close()
                else:
                    self.dosend('Good :)')
            self.dosend(flag)
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
