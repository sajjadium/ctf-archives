#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long as bl, long_to_bytes as lb
from Crypto.Cipher import AES
import os
import random
import string

sp = list(map(ord, list(string.printable)))

def pad(msg):
    pad_length = random.randint(20, 100)
    for i in range(pad_length):
        c = random.randint(0, 255)
        while c in sp:
            c = random.randint(0, 255)
        pos = random.randint(0, len(msg) - 1)
        msg = msg[:pos] + chr(c).encode() + msg[pos:]
    while True:
        c = random.randint(0, 255)
        while c in sp:
            c = random.randint(0, 255)
        pos = random.randint(0, len(msg) - 1)
        msg = msg[:pos] + chr(c).encode() + msg[pos:]
        if (len(msg) % 16 == 0):
            break
    return msg

class Person:
    def make_public_part(self, g, p):
        return pow(g, self.secret, p)

    def make_private_part(self, gx, p):
        self.key = pow(gx, self.secret, p) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        self.key = lb(self.key)
        while (len(self.key) != 16):
            self.key += b'\x01'
        return self.key

    def send_message(self, msg):
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        enc = iv + cipher.encrypt(pad(msg))
        return enc
    
    def receive_message(self, enc_message):
        try:
            iv = enc_message[:16]
            enc = enc_message[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            msg = cipher.decrypt(enc)
            return 'Message received!'
        except:
            return 'Message not received!'

class Alice(Person):
    def __init__(self):
        self.secret = 0 # REDACTED

class Bob(Person):
    def __init__(self):
        self.secret = 0 # REDACTED
        assert 2 < self.secret < 100

class You(Person):
    def __init__(self, secret):
        self.secret = secret
