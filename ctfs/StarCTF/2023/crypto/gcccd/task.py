#!/usr/bin/env python3

from secret import flag
import socketserver
import hashlib
import signal
import random
import string
import os

p=20973268502876719886012765513713011996343752519737224550553652605696573094756255499211333096502971357908939298357512380813773140436677393056575164230564778609423872301899323721040416852230597466288892977839300189625522429038289083381035647126860128821615664730513694930502000903655609105029016636999073477487851081722316115785141
enc=lambda x:pow(17,x,p)
m=int(flag.encode().hex(),16)

def gcd(a,b,f=enc):
    if b:
        return gcd(b,a%b,f)
    else:
        return f(a)

class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def timeout_handler(self, signum, frame):
        self.request.close()

    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
        _hexdigest = hashlib.sha256(proof.encode()).hexdigest()
        self.request.send(f"sha256(XXXX+{proof[4:]}) == {_hexdigest}\n".encode()+b'Give me XXXX: ')
        x = self.request.recv(1024).strip(b'\n')
        if len(x) != 4 or hashlib.sha256(x+proof[4:].encode()).hexdigest() != _hexdigest:
            return False
        return True

    def handle(self):
        signal.alarm(60)

        if not self.proof_of_work():
            return

        while True:
            try:
                self.request.send(b'type:')
                t=int(self.request.recv(1024).strip(b'\n'))
                self.request.send(b'a:')
                a=int(self.request.recv(1024).strip(b'\n'))
                self.request.send(b'b:')
                b=int(self.request.recv(1024).strip(b'\n'))
                assert a>0 and b>0
                if t==1:#enc test
                    self.request.send(b'%d\n'%gcd(a,b))
                elif t==2:#leak try1
                    self.request.send(b'%d\n'%gcd(a,m))
                elif t==3:#leak try2
                    self.request.send(b'%d\n'%gcd(a,b,f=lambda x:gcd(x,m)))
                elif t==4:#leak try3
                    self.request.send(b'%d\n'%gcd(a,m,f=lambda x:gcd(x,b)))
                else:
                    self.request.close()
                    break
            except BrokenPipeError:
                break
            except:
                self.request.send(b'Bad input!\n')


class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 23333
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()