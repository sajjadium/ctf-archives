#!/usr/bin/env python3

import signal
import socketserver
import string
import os
from secret import flag
from py_ecc import bn128

lib = bn128
FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
  lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply
pairing, neg = lib.pairing, lib.neg

LENGTH = 7


def Cx(x,length=LENGTH):
    res = []
    for i in range(length):
        res.append(pow(x,i,curve_order) % curve_order)
    return res

def C(x,y,length=LENGTH):
    assert len(x) == len(y) == length
    res = multiply(G1, curve_order)
    for i in range(length):
        res = add(multiply(x[i],y[i]),res) 
    return res 

def Z(x):
    return (x-1)*(x-2)*(x-3)*(x-4) % curve_order


def genK(curve_order,length=LENGTH):
    t = int(os.urandom(8).hex(),16) % curve_order
    a = int(os.urandom(8).hex(),16) % curve_order
    Ct = Cx(t)
    PKC = []
    for ct in Ct:
        PKC.append(multiply(G1, ct))
    PKCa = []
    for ct in Ct:
        PKCa.append(multiply(multiply(G1, ct), a))

    PK = (PKC,PKCa)
    VKa = multiply(G2, a)
    VKz = multiply(G2, Z(t))
    VK = (VKa,VKz)
    return PK,VK

def verify(proof,VK):
    VKa,VKz = VK
    PiC,PiCa,PiH = proof

    l = pairing(VKa, PiC)
    r = pairing(G2, PiCa)
    if l !=r:
        return False
    l = pairing(G2,PiC)
    r = pairing(VKz,PiH)
    if l !=r:
        return False
    return True


class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)


    def OKPROOF(self,proof,VK):
        return verify(proof,VK)


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
            self.dosend('===========================')
            self.dosend('=WELCOME TO 0KPR00F SYSTEM=')
            self.dosend('===========================')
            PK,VK = genK(curve_order)
            self.dosend(str(PK))
            self.dosend('now give me your proof')
            msg = self.request.recv(1024).strip()
            msg = msg.decode('utf-8')
            tmp = msg.replace('(','').replace(')','').replace(',','')
            tmp = tmp.split(' ')
            assert len(tmp) == 6
            PiC = (FQ(int(tmp[0].strip())),FQ(int(tmp[1].strip())))
            PiCa = (FQ(int(tmp[2].strip())),FQ(int(tmp[3].strip())))
            PiH = (FQ(int(tmp[4].strip())),FQ(int(tmp[5].strip())))
            proof = (PiC,PiCa,PiH)
            if self.OKPROOF(proof,VK):
                self.dosend("Congratulations！Here is flag:"+flag)
            else:
                self.dosend("sorry")
            

        except TimeoutError:
            self.dosend('Timeout!')
            self.request.close()
        except:
            self.dosend('Wtf?')
            self.request.close()


class ThreadedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 13337
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()