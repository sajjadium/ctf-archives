#!/usr/bin/env python3

import random
import signal
import socketserver
import string
from Crypto.Util.number import *
from hashlib import sha256
from secret import FLAG
from os import urandom

P_BITS = 512
E_BITS = int(P_BITS * 2 * 0.292) + 30
CNT_MAX = 7

class LCG:
    def __init__(self):
        self.init()

    def next(self):
        out = self.s[0]
        self.s = self.s[1: ] + [(sum([i * j for (i, j) in zip(self.a, self.s)]) + self.b) % self.p]
        return out

    def init(self):
        while True:
            p = getPrime(2 * P_BITS)
            if p.bit_length() == 2 * P_BITS:
                self.p = p
                break
        self.b = getRandomRange(1, self.p)
        self.a = [getRandomRange(1, self.p) for _ in range(6)]
        self.s = [getRandomRange(1, self.p) for _ in range(6)]

class RSA:
    def __init__(self, l, p = 0, q = 0):
        self.l = l
        if not p:
            while True:
                p = getPrime(P_BITS)
                if p.bit_length() == P_BITS:
                    self.p = p
                    break
            while True:
                p = getPrime(P_BITS)
                if p.bit_length() == P_BITS:
                    self.q = p
                    break
        else:
            self.p = abs(p)
            self.q = abs(q)
        self.e = getPrime(E_BITS)
        self.check()

    def enc(self, m):
        return pow(m, self.e, self.n)

    def noisy_enc(self, m, r = 1):
        if r:
            self.refresh()
        return pow(m, self.e ^ self.l.next(), self.n)

    def dec(self, c):
        return pow(c, self.d, self.n)
        
    def check(self):
        assert self.p.bit_length() == P_BITS
        assert self.q.bit_length() == P_BITS
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        assert self.e.bit_length() >= E_BITS
        assert self.e < self.phi
        assert GCD(self.e, self.phi) == 1
        self.d = inverse(self.e, self.phi)
        assert self.d.bit_length() >= E_BITS
        for _ in range(20):
            x = self.l.next() % self.n
            assert self.dec(self.enc(x)) == x

    def refresh(self):
        self.e = (self.e ^ self.l.next()) % (2**E_BITS)

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

    def recv_hex(self, l):
        return int(self.recvn(l + 1), 16)

    def handle(self):
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(60)
            if not self.proof_of_work():
                self.dosend('You must pass the PoW!')
                return

            signal.alarm(20)
            self.dosend('Give me your RSA key plz.')
            pq = [self.recv_hex(P_BITS // 4) for _ in range(2)]
            lcg = LCG()
            alice = RSA(lcg)
            bob = RSA(lcg, *pq)
            secrets = getRandomNBitInteger(P_BITS // 8)
            secrets_ct = alice.enc(secrets)
            self.dosend('{}\n{}'.format(alice.e, alice.n))
            self.dosend('{}\n{}\n{}\n{}'.format(lcg.p, lcg.a, lcg.b, lcg.s))
            
            CNT = 0
            while CNT < CNT_MAX:
                self.dosend('pt: ')
                pt = self.recv_hex(P_BITS // 2)
                if pt == 0:
                    break
                ct = alice.noisy_enc(pt)
                ct = bob.noisy_enc(ct)
                self.dosend('ct: ' + hex(ct))
                CNT += 1
            print(secrets_ct)
            secrets_ct = bob.noisy_enc(secrets_ct)
            self.dosend('secrets_ct: ' + hex(secrets_ct))
            lcg.init()
            bob = RSA(lcg, *pq)
            self.dosend('{}\n{}\n{}\n{}'.format(lcg.p, lcg.a, lcg.b, lcg.s))

            seen = set()
            while CNT < CNT_MAX:
                self.dosend('ct: ')
                ct = self.recv_hex(P_BITS // 2)
                if ct == 0:
                    break
                pt = alice.dec(ct)
                if pt in seen:
                    self.dosend('You can only decrypt each ciphertext once.')
                    self.request.close()
                else:
                    seen.add(pt)
                pt = bob.noisy_enc(pt)
                self.dosend('pt: ' + hex(pt))
                CNT += 1            
            
            guess = self.recv_hex(P_BITS // 4)
            if guess == secrets:
                self.dosend('Wow, how do you know that?')
                self.dosend('Here is the flag: ' + FLAG)
            else:
                self.dosend('Wrong!')
        except TimeoutError:
            self.dosend('Timeout!')
        except:
            self.dosend('GG')
        self.request.close()

class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 32226
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()