#!/usr/bin/env python3
import multiprocessing
import os
import signal
import socket
import re

assert os.path.isfile("secret/password.txt"), "Password file not found."

MAX_SIZE = 0x1000
LOGIN_USERS = {
    b'guest': b'guest',
    b'admin': open("secret/password.txt", "rb").read().strip()
}
PROTECTED = [b"server.py", b"secret"]

assert re.fullmatch(b"[0-9a-f]+", LOGIN_USERS[b'admin'])

class Timeout(object):
    def __init__(self, seconds):
        self.seconds = seconds

    def handle_timeout(self, signum, frame):
        raise TimeoutError('Timeout')

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
        return self

    def __exit__(self, _type, _value, _traceback):
        signal.alarm(0)

class PyNetworkFS(object):
    def __init__(self, conn):
        self._conn = conn
        self._auth = False
        self._user = None

    def __del__(self):
        self._conn.close()

    @property
    def is_authenticated(self):
        return self._auth

    @property
    def is_admin(self):
        return self.is_authenticated and self._user == b'admin'

    def response(self, message):
        self._conn.send(message)

    def recvline(self):
        data = b''
        while True:
            match self._conn.recv(1):
                case b'': return None
                case b'\n': break
                case byte: data += byte
        return data

    def authenticate(self):
        """Login prompt"""
        username = password = b''
        with Timeout(30):
            # Receive username
            self.response(b"Username: ")
            username = self.recvline()
            if username is None: return

            if username in LOGIN_USERS:
                password = LOGIN_USERS[username]
            else:
                self.response(b"No such a user exists.\n")
                return

        with Timeout(30):
            # Receive password
            self.response(b"Password: ")
            i = 0
            while i < len(password):
                c = self._conn.recv(1)
                if c == b'':
                    return
                elif c != password[i:i+1]:
                    self.response(b"Incorrect password.\n")
                    return
                i += 1

            if self._conn.recv(1) != b'\n':
                self.response(b"Incorrect password.\n")
                return

        self.response(b"Logged in.\n")
        self._auth = True
        self._user = username

    def serve(self):
        """Serve files"""
        with Timeout(60):
            while True:
                # Receive filepath
                self.response(b"File: ")
                filepath = self.recvline()
                if filepath is None: return

                # Check filepath
                if not self.is_admin and \
                   any(map(lambda name: name in filepath, PROTECTED)):
                    self.response(b"Permission denied.\n")
                    continue

                # Serve file
                try:
                    f = open(filepath, 'rb')
                except FileNotFoundError:
                    self.response(b"File not found.\n")
                    continue
                except PermissionError:
                    self.response(b"Permission denied.\n")
                    continue
                except:
                    self.response(b"System error.\n")
                    continue

                try:
                    self.response(f.read(MAX_SIZE))
                except OSError:
                    self.response(b"System error.\n")
                finally:
                    f.close()

def pynetfs_main(conn):
    nfs = PyNetworkFS(conn)
    try:
        nfs.authenticate()
    except TimeoutError:
        nfs.response(b'Login timeout.\n')

    if nfs.is_authenticated:
        try:
            nfs.serve()
        except TimeoutError:
            return

if __name__ == '__main__':
    # Setup server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    print("Listening on 0.0.0.0:10021")
    sock.bind(('0.0.0.0', 10021))
    sock.listen(16)

    # Handle connection
    ps = []
    while True:
        conn, addr = sock.accept()
        ps.append(multiprocessing.Process(target=pynetfs_main, args=(conn,)))
        ps[-1].start()
        conn.close()
        ps = list(filter(lambda p: p.is_alive() or p.join(), ps))
