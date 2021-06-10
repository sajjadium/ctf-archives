#!/usr/bin/python3

#Super Cool Facts Server
#author: cybears_cipher

#python3 SuperCoolFactsServer.py

#requirements
#pip3 install pycrypto

## SERVER
# socat TCP-LISTEN:3141,reuseaddr,fork EXEC:"python3 ./SuperCoolFactsServer.py"

##CLIENT
# nc localhost 3141

import os
from random import SystemRandom, choice
import json
import EC
import Crypto.Cipher.AES as AES
import hashlib
from binascii import *

from SuperCoolFactsSecret import flag, cool_facts

randrange = SystemRandom().randrange

def pad(data,blocksize):
    padlen = blocksize - (len(data)%blocksize)
    return data + (padlen.to_bytes(1,byteorder="little"))*padlen

# Key Derivation Function
# input: Elliptic curve point (from EC library)
# output: 16-byte AES key
def kdf(shared_point):
    s = str(shared_point.x) + str(shared_point.y)
    return hashlib.sha1(s.encode("utf-8")).digest()[0:16]

def encrypt_message(message, key):
    iv = os.urandom(16)
    pmessage = pad(message,16)

    a = AES.new(key, IV=iv, mode=AES.MODE_CBC)
    cipher = a.encrypt(pmessage)
    return {'iv':hexlify(iv).decode("utf-8"), 'cipher':hexlify(cipher).decode("utf-8")}

def decrypt_message(cipher, key, iv):
    a = AES.new(key, IV=iv, mode=AES.MODE_CBC)
    plain = a.decrypt(cipher)
    return plain

def print_menu():
    print("\nWelcome to the Super Cool Facts Server. Enter your choice:\n"
          "(0) Print Cryptographic Parameters\n"
          "(1) Perform ECDH handshake with server\n"
          "(2) Get a Super Cool Fact!\n"
          "(3) Submit hash of private key for flag\n"
          "(q) quit\n")

def print_crypto_params():
    print("params are:" + "\n")
    print(" Elliptic curve E: y^2 = x^3 + ax + b mod p \n")
    print("  p = {}".format(EC.p))
    print("  a = {}".format(EC.a))
    print("  b = {}".format(EC.b))
    print(" Elliptic Curve G = (gx, gy) on E \n")
    print("  gx = {}".format(EC.gx))
    print("  gy = {}".format(EC.gy))

class Server:
    def __init__(this):
        this.handshake_done = False
        this.key = None
        this.privkey = randrange(2,EC.order)
        this.pubkey = EC.ec_scalar(EC.E, this.privkey, EC.G)
        this.hash_privkey = hashlib.sha1(str(this.privkey).encode("utf-8")).hexdigest()

if __name__ == "__main__":

    cmd = ""
    S = Server()

    while cmd != "q":
        print_menu()
        cmd = input("Enter a value: ").strip()

        #Print crypto parameters
        if cmd == "0":
            print_crypto_params()
            continue

        #Perform ECDH handshake with server
        if cmd == "1":
            print("My public point:")
            j = {"x":S.pubkey.x, "y":S.pubkey.y}
            print(json.dumps(j))
            sender_public = input("Provide your public point:")

            try:
                spub = json.loads(sender_public)
            except Exception as e:
                print(e.args[0] +": JSON Error - quitting")
                exit()

            try:
                if ('x' not in spub.keys()) or ('y' not in spub.keys()):
                    print("ERROR: need x,y keys in json")
                    exit()
            except Exception as e:
                print(e.args[0] +": JSON Error II - quitting")
                exit()

            if (type(spub['x']) != int) or (type(spub['y']) != int):
                print("ERROR: x and y should be ints")
                exit()

            spub_point = EC.ec_point(EC.E, spub['x'], spub['y'])
            shared_point = EC.ec_scalar(EC.E, S.privkey, spub_point)

            S.key = kdf(shared_point)
            S.handshake_done = True

            continue

        #Get Super Cool Fact!
        if cmd == "2":
            if S.handshake_done == False:
                print("Need to perform handshake first!")
                continue

            cf = choice(cool_facts)

            cipher = encrypt_message(cf.encode("utf-8"), S.key)
            print(json.dumps(cipher))
            continue

        #Submit hash of private key for flag
        if cmd == "3":
            print("Provide the hex encoded SHA1 hash of the private key...")
            print('Something like: hashlib.sha1(str(privkey).encode("utf-8")).hexdigest()')
            answer = input().strip()
            if answer == S.hash_privkey:
                print("SUCCESS! Here's your flag: " + flag)
            else:
                print("INCORRECT")
            exit()

        if cmd == "q":
            exit()

        print("Incorrect option\n")

    exit()
