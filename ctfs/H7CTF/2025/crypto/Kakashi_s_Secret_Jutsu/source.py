#!/usr/bin/env python3
import socketserver
import signal
import string, random
from hashlib import sha256

from Crypto.Cipher import AES
from secret import get_key, get_IV, get_secret, get_flag, perform_encryption

KAKASHI_BANNER = br"""
 /$$   /$$ /$$$$$$$$ /$$$$$$  /$$$$$$$$ /$$$$$$$$
| $$  | $$|_____ $$//$$__  $$|__  $$__/| $$_____/
| $$  | $$     /$$/| $$  \__/   | $$   | $$      
| $$$$$$$$    /$$/ | $$         | $$   | $$$$$   
| $$__  $$   /$$/  | $$         | $$   | $$__/   
| $$  | $$  /$$/   | $$    $$   | $$   | $$      
| $$  | $$ /$$/    |  $$$$$$/   | $$   | $$      
|__/  |__/|__/      \______/    |__/   |__/
"""

JUTSU_MENU = br"""
1. Perform Jutsu
2. Test Your Sharingan
3. Die
"""

class KakashiTask(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def recvhex(self, prompt=b'> '):
        self.send(prompt, newline=False)
        try:
            data = bytes.fromhex(self._recvall().decode('latin-1'))
        except ValueError as e:
            self.send(b"Wrong hex value!")
            self.close()
            return None
        return data

    def close(self):
        self.send(b"Farewell, shinobi~")
        self.request.close()

    def pad(self, data):
        pad_len = 16 - len(data)%16
        return data + bytes([pad_len])*pad_len

    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
        _hexdigest = sha256(proof.encode()).hexdigest()

        self.send(f"sha256(XXXX+{proof[4:]}) == {_hexdigest}".encode())
        x = self.recv(prompt=b'Give me XXXX: ')
        if len(x) != 4 or sha256(x+proof[4:].encode()).hexdigest() != _hexdigest:
            return False
        return True

    def handle(self):
        signal.alarm(1200)

        self.send(KAKASHI_BANNER)
        if not self.proof_of_work():
            return

        secret = get_secret()
        key = get_key()
        IV = get_IV()
        flag = get_flag()
        aes = AES.new(key, mode=AES.MODE_CBC, iv=IV)
        self.send(f"Kakashi says — IV is: {IV.hex()}".encode())
        self.send(b"If your Sharingan can read the secret, bring it to me and I shall reward you with a scroll~!")

        while True:
            self.send(JUTSU_MENU, newline=False)
            choice = self.recv()

            if choice == b"1":
                msg = self.recvhex(prompt=b"Your jutsu (in hex): ")
                if not msg: break
                cipher = perform_encryption(aes, msg, secret, self.pad)
                self.send(cipher.hex().encode())
                continue
            elif choice == b"2":
                guess = self.recvhex(prompt=b"What did your Sharingan see? (in hex): ")
                if not guess: break
                if guess == secret:
                    self.send(b"Kakashi: Impressive. Here is your scroll : " + flag)
                else:
                    self.send(b"H7CTF{Wrong_Guess!}")

            self.close()
            break

class KakashiThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class KakashiForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10000
    server = KakashiForkedServer((HOST, PORT), KakashiTask)
    server.allow_reuse_address = True
    server.serve_forever()