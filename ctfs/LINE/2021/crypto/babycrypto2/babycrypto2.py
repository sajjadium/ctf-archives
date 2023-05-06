#!/usr/bin/env python
from base64 import b64decode
from base64 import b64encode
import socket
import multiprocessing

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import sys

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data, 
            AES.block_size)))

    def encrypt_iv(self, data, iv):
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data, 
            AES.block_size)))

    def decrypt(self, data):
        raw = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)

flag = open("flag", "rb").read().strip()

AES_KEY = get_random_bytes(AES.block_size)
TOKEN = b64encode(get_random_bytes(AES.block_size*10-1))
COMMAND = [b'test',b'show']
PREFIX = b'Command: '

def run_server(client):
    client.send(b'test Command: ' + AESCipher(AES_KEY).encrypt(PREFIX+COMMAND[0]+TOKEN) + b'\n')
    while(True):
        client.send(b'Enter your command: ')
        tt = client.recv(1024).strip()
        tt2 = AESCipher(AES_KEY).decrypt(tt)
        client.send(tt2 + b'\n')
        if tt2 == PREFIX+COMMAND[1]+TOKEN:
            client.send(b'The flag is: ' + flag)
            client.close()
            break

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 16002))
    server.listen(1)

    while True:
        client, address = server.accept()

        process = multiprocessing.Process(target=run_server, args=(client, ))
        process.daemon = True
        process.start()