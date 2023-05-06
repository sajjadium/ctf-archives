#!/usr/bin/python3
import os
import socketserver
import random
import signal
import string
import struct
from hashlib import sha256
import secrets
import pykeepass

from flag import flag

MAXSIZE = 0x2000

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

    def askfor(self, msg):
        self.request.sendall(msg)
        return self.request.recv(0x20).strip().decode('latin-1')

    def recvint(self):
        try:
            return int(self.request.recv(10))
        except:
            return 0

    def recvblob(self):
        self.request.sendall(b"size: ")
        sz = self.recvint()
        assert sz < MAXSIZE
        self.request.sendall(b"blob(hex): ")
        sz = sz*2+1
        r = sz
        res = b''
        while r>0:
            res += self.request.recv(r)
            r = sz - len(res)
        return bytes.fromhex(res.strip().decode('latin-1'))

    def prepared(self):
        client_ip = self.client_address[0]
        dname = sha256(client_ip.encode('latin-1')).hexdigest()
        self.d = os.path.join("/tmp", dname)
        os.makedirs(self.d, exist_ok=True)
        self.f = os.path.join(self.d, "a.kdbx")

    def handle(self):
        signal.alarm(20)
        if not self.proof_of_work():
            return
        signal.alarm(20)
        self.request.sendall(b"Welcome to our cloud password storage service.\nNotice that storage size is strictly limited for free trial >_<\n")
        self.prepared()
        self.request.sendall(b"master password: ")
        password = self.request.recv(0x40).strip().decode('latin-1')
        if not os.path.exists(self.f):
            answer = self.askfor(b"Do you already have a database to import? (y/N) ")
            if answer[0] == 'y':
                file = self.recvblob()
                with open(self.f, 'wb') as f:
                    f.write(file)
            else:
                pykeepass.create_database(self.f, password)
        try:
            db = pykeepass.PyKeePass(self.f, password)
        except:
            self.request.sendall(b"[error] Invalid master password!\n")
            self.request.sendall(b"We never store your master password for safety, and cannot help you recover it :(\n")
            answer = self.askfor(b"Do you want to delete your database? (y/N) ")
            if answer[0] == 'y':
                os.remove(self.f)
            self.request.close()
            return
        for _ in range(0x100):
            self.request.sendall(b"> ")
            cmd = self.request.recv(0x20).strip()
            if cmd == b"add_entry":
                gn = self.askfor(b"dest group: ")
                g = db.root_group if gn == "" else db.find_groups_by_name(gn, first=True)
                t = self.askfor(b"title: ")
                u = self.askfor(b"username: ")
                p = self.askfor(b"password: ")
                db.add_entry(g, t, u, p)
            elif cmd == b"add_group":
                gn = self.askfor(b"dest group: ")
                g = db.root_group if gn == "" else db.find_groups_by_name(gn, first=True)
                n = self.askfor(b"name: ")
                db.add_group(g, n)
            elif cmd == b"add_binary":
                blob = self.recvblob()
                db.add_binary(blob)
            elif cmd == b"find_entries":
                t = self.askfor(b"title: ")
                res = db.find_entries_by_title(t)
                if len(res) > 0:
                    self.request.sendall(str(res[0]).encode('latin-1')+b'\n')
            elif cmd == b"find_groups":
                n = self.askfor(b"name: ")
                res = db.find_groups_by_name(n)
                if len(res) > 0:
                    self.request.sendall(str(res[0]).encode('latin-1')+b'\n')
            elif cmd == b"gimme_flag":
                db.add_entry(db.root_group, "flag", "0ops", flag)
                db.password = secrets.token_hex(32)
            elif cmd == b"list_entries":
                self.request.sendall(str(db.entries).encode('latin-1')+b'\n')
            elif cmd == b"list_groups":
                self.request.sendall(str(db.groups).encode('latin-1')+b'\n')
            elif cmd == b"list_binaries":
                self.request.sendall(str(db.binaries).encode('latin-1')+b'\n')
            elif cmd == b"leave":
                answer = self.askfor(b"Do you need to backup your database elsewhere? (y/N) ")
                if answer[0] == 'y':
                    with open(self.f, 'rb') as f:
                        cont = f.read()
                    self.request.sendall(cont.hex().encode('latin-1')+b'\n')
                break
            else:
                break
            db.save()
            if os.stat(self.f).st_size > MAXSIZE:
                self.request.sendall(b"[error] Filesize limit exceeded!")
                os.remove(self.f)
                break
        self.request.close()

class ForkedServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
