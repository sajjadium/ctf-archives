#!/usr/bin/python3
import os
import socketserver
import random
import signal
import string
import tempfile
import tarfile
from hashlib import sha256
from Crypto.Cipher import ChaCha20

from secret import flag,key

MAXNUM = 9
MAXFILESZ = 100
MAXTARSZ = 100000

class LicenseRequired(Exception):
	pass

class Task(socketserver.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
        digest = sha256(proof.encode('latin-1')).hexdigest()
        self.request.send(str.encode("sha256(XXXX+%s) == %s\n" % (proof[4:],digest)))
        self.request.send(str.encode('Give me XXXX:'))
        x = self.request.recv(10).decode()
        x = x.strip()
        xx = x+proof[4:]
        if len(x) != 4 or sha256(xx.encode('latin-1')).hexdigest() != digest:
            return False
        return True

    def recvint(self):
        try:
            return int(self.request.recv(10))
        except:
            return 0

    def recvfile(self, maxsz):
        self.request.sendall(b"size: ")
        sz = self.recvint()
        assert sz < maxsz
        self.request.sendall(b"file(hex): ")
        r = 2*sz+1
        res = b''
        while r > len(res):
            res += self.request.recv(r)
        dat = bytes.fromhex(res.strip().decode('latin-1'))
        return dat

    def savefile(self, name, dat):
        fname = os.path.join(self.dir, name)
        with open(fname, "wb") as f:
            f.write(dat)
        self.request.sendall(f"[OK] {name} added\n".encode('latin-1'))

    def addsec(self):
        if len(self.data) > MAXNUM:
            self.request.sendall(b"[Error] too many secrets\n")
            raise LicenseRequired
        name = os.urandom(4).hex()
        self.data[name] = 1
        dat = self.recvfile(MAXFILESZ)
        self.savefile(name, dat)

    def upload(self):
        dat = self.recvfile(MAXTARSZ)
        c = ChaCha20.new(nonce=dat[:8], key=key)
        pt = c.decrypt(dat[8:])
        self.savefile("a.tar", pt)
        tname = os.path.join(self.dir, "a.tar")
        if not tarfile.is_tarfile(tname):
            self.request.sendall(b"[Error] not tar file\n")
            self.request.sendall(pt.hex().encode('latin-1')+b'\n')
            return
        f = tarfile.open(tname)
        cnt = 0
        for fname in f.getnames():
            if fname.startswith('/') or '..' in fname:
                self.request.sendall(b"[Error] you need a license to hack us\n")
                raise LicenseRequired
            cnt += 1
            if cnt > MAXNUM:
                break
        if len(self.data) + cnt > MAXNUM:
            self.request.sendall(b"[Error] too many files\n")
            raise LicenseRequired
        for fname in f.getnames():
            self.data[fname] = 1
        f.extractall(path=self.dir)
        os.unlink(tname)
        self.request.sendall(b"[OK] upload succeeded\n")

    def readsec(self):
        raise LicenseRequired

    def download(self):
        nonce = True
        for name in self.data:
            if self.data[name] == 0:
                nonce = False
        fname = os.path.join(self.dir, "a.tar")
        with tarfile.open("a.tar", 'w') as f:
            for name in self.data:
                f.add(name)
        with open(fname, 'rb') as f:
            cont = f.read()
        c = ChaCha20.new(key=key)
        dat = c.encrypt(cont)
        if nonce:
            dat = c.nonce+dat
        self.request.sendall(f"[OK] ctar file size: {len(dat)}\n".encode('latin-1'))
        self.request.sendall(dat.hex().encode('latin-1')+b'\n')

    def addflag(self):
        if len(self.data) > MAXNUM:
            self.request.sendall(b"[Error] too many secrets\n")
            raise LicenseRequired
        name = os.urandom(4).hex()
        self.data[name] = 0
        self.savefile(name, flag)

    def handle(self):
        if not self.proof_of_work():
            return
        self.data = {}
        self.dir = tempfile.mkdtemp()
        os.chdir(self.dir)
        signal.alarm(120)
        self.request.sendall(b"*** Welcome to ctar service ***\nUpload and archive your secrets with our super fancy homemade secure tar file format. You'll like it\nNotice: the file size is limited in your free trial\n")
        while True:
            try:
                self.request.sendall(b"1. add your secret\n2. upload ctar file\n3. read secrets\n4. download ctar file\n0. add flag\n> ")
                i = self.recvint()
                if i==1:
                    self.addsec()
                elif i==2:
                    self.upload()
                elif i==3:
                    self.readsec()
                elif i==4:
                    self.download()
                elif i==0:
                    self.addflag()
                else:
                    break
            except:
                pass
        os.system(f"rm -r {self.dir}")
        self.request.close()

class ForkedServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
