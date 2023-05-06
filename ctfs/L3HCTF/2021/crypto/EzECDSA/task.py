import gmpy2
import hashlib
import socketserver
import os,random,string
from hashlib import sha256
from Crypto.Util.number import bytes_to_long

from SECRET import FLAG

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
xG = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
yG = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
h = 1
zero = (0,0)
G = (xG, yG)
kbits = 8

def add(p1, p2):
    if p1 == zero:
        return p2
    if p2 == zero:
        return p1
    (p1x,p1y),(p2x,p2y) = p1,p2
    if p1x == p2x and (p1y != p2y or p1y == 0):
        return zero
    if p1x == p2x:
        tmp = (3 * p1x * p1x + a) * gmpy2.invert(2 * p1y , p) % p
    else:
        tmp = (p2y - p1y) * gmpy2.invert(p2x - p1x , p) % p
    x = (tmp * tmp - p1x - p2x) % p
    y = (tmp * (p1x - x) - p1y) % p
    return (int(x),int(y))

def mul(n, p):
    r = zero
    tmp = p
    while 0 < n:
        if n & 1 == 1:
            r = add(r,tmp)
        n, tmp = n >> 1, add(tmp,tmp)
    return r

def sha256(raw_message):
    return hashlib.sha256(raw_message).hexdigest().encode()

def _sha256(raw_message):
    return bytes_to_long(hashlib.sha256(raw_message).digest())

class Task(socketserver.BaseRequestHandler):
    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)]).encode()
        digest = sha256(proof)
        self.request.send(b"sha256(XXXX+%b) == %b\n" % (proof[4:],digest))
        self.request.send(b'Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 4 or sha256(x+proof[4:]) != digest: 
            return False
        return True
    
    def recvall(self, sz):
        try:
            r = sz
            res = ""
            while r > 0:
                res += self.request.recv(r).decode()
                if res.endswith("\n"):
                    r = 0
                else:
                    r = sz - len(res)
            res = res.strip()
        except:
            res = ""
        return res.strip("\n")

    def dosend(self, msg):
        self.request.sendall(msg)

    def handle(self):
        try:
            if not self.proof_of_work():
                return

            dA = random.randrange(n)
            Public_key = mul(dA, G)
            self.dosend(str(Public_key).encode() + b'\n')
            
            for _ in range(100):
                self.dosend(b"Give me your message:\n")
                msg = self.recvall(100)
                hash = _sha256(msg.encode())
                k = random.randrange(n)
                kp = k % (2 ** kbits)
                P = mul(k, G)
                r_sig = P[0]
                k_inv = gmpy2.invert(k, n)
                s_sig = (k_inv * (hash + r_sig * dA)) % n
                self.dosend(b"r = " + str(r_sig).encode() + b'\n')
                self.dosend(b"s = " + str(s_sig).encode() + b'\n')
                self.dosend(b"kp = " + str(kp).encode() + b'\n')
                self.dosend(b"hash = " + str(hash).encode() + b'\n')
            
            self.dosend(b"Give me dA\n")
            private_key = self.recvall(300)
            if int(private_key) == dA:
                self.dosend(FLAG)

        except:
            self.dosend(b"Something error!\n")
            self.request.close()

class ForkingServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 23333
    server = ForkingServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()