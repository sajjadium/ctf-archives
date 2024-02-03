#!/usr/local/bin/python

import sys
import math
import hashlib
import binascii
import re

from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA

class Server(object):
    
    def __init__(self):
        
        with open("key.pem") as key:
            self.key = RSA.importKey(key.read())
        

        with open("./flag.txt") as ifile:
            flag = ifile.read()
        flag = bytes_to_long(flag.encode('utf-8'))

        c = pow(flag, self.key.e, self.key.n)
        
        sha = hashlib.sha256()
        sha.update(long_to_bytes(c))

        self.seen_hashes = [sha.hexdigest()]
        
        print("Welcome to Olivia's Shared Message Encryption System")
        print(f"Ciphertext of Flag: {c}")


    def encrypt_message(self, msg):

        try:
            msg = int(msg)
            ctx = pow(msg, self.key.e, self.key.n)
        except:
            print("Invalid plaintext")
            return False

        print(ctx)
        sys.stdout.flush()

        return True

    def decrypt_message(self, msg):
        
        try:
            msg = int(msg)

            sha = hashlib.sha256()
            sha.update(long_to_bytes(msg))
            h = sha.hexdigest()

            if h in self.seen_hashes:
                return False

        
            self.see_hash(h)
            p = pow(msg, self.key.d, self.key.n)
        except:
            print("Invalid Ciphertext")
            return False

        print(p)
        sys.stdout.flush()

        return True

    def see_hash(self, hash):
        if len(self.seen_hashes) >= 50:
            sys.stderr.write("Too many messages sent at once\n")
            sys.exit(1)
        self.seen_hashes.append(hash)

    def handle_encrypt_message(self, msg):
        msg = msg.split(':')
        _, smsg = msg
        
        if not self.encrypt_message(smsg):
            print("MESSAGE FAIL") 
            sys.stdout.flush()
            return

    def handle_decrypt_message(self, msg):
        msg = msg.split(':')
        _, rmsg = msg

        if not self.decrypt_message(rmsg):
            print("FAILED TO RECEIVE MESSAGE")
            sys.stdout.flush()
            return

    def handle_key_message(self):
        n = self.key.n
        e = self.key.e

        print("N:%s\nE:%s\n" % (n, e))
        sys.stdout.flush()

    def serve(self):
        while 1:
            msg = input()

            if msg.startswith("ENCRYPT:"):
                self.handle_encrypt_message(msg)
            elif msg.startswith("DECRYPT:"):
                self.handle_decrypt_message(msg)
            elif msg.startswith("KEY:"):
                self.handle_key_message()
            else:
                print("BAD API COMMAND")
                continue


if __name__ == "__main__":
    s = Server()

    s.serve()
