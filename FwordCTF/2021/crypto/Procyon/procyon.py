#!/usr/bin/env python3.8
from Crypto.Util.number import getStrongPrime, bytes_to_long, inverse
from json import loads, dumps
from time import time
import os, sys, hashlib, random, signal

FLAG = "FwordCTF{####################################################}"
assert len(FLAG) < 1024//8

prime = getStrongPrime(1024)

class DiffieHellman:
    def __init__(self):
        self.p = prime
        self.g = 3
        self.private_key = random.randrange(2, self.p - 1)
        self.public_key = pow(self.g, self.private_key, self.p)

    def shared_secret(self, K):
        return pow(K, self.private_key, self.p)

def proof(msg, secret):
    m = bytes_to_long(msg)
    t = int(time())
    return t*secret + m*secret % prime


class Procyon:
    def __init__(self):
        self.Alice = DiffieHellman()
        self.Bob = DiffieHellman()

    def start(self):
        Alice_params = {"g": hex(self.Alice.g), "A": hex(self.Alice.public_key), "p": hex(self.Alice.p)}
        print(f"Alice sends to Bob : {dumps(Alice_params)}\n")
        Bob_params = {"g": hex(self.Bob.g), "B": hex(self.Bob.public_key), "p": hex(self.Bob.p)}
        print(f"Bob sends to Alice : {dumps(Bob_params)}\n")

        shared_secret = self.Alice.shared_secret(int(Bob_params['B'], 16))

        print(f"Intercepted message : {hex(proof(FLAG.encode(), shared_secret))}\n")
        
        try:
            print("Now it's your turn to talk to Bob.")
            while True:
                params = loads(input("Send your parameters to Bob : "))
                assert int(params['p'], 16) == self.Alice.p
                assert int(params['g'], 16) == self.Alice.g
                assert int(params['pub'], 16) != self.Alice.public_key

                shared_secret = self.Bob.shared_secret(int(params['pub'], 16))

                if int(params['pub'], 16) == self.Alice.public_key:
                    print(f"\nIntercepted message : {hex(proof(FLAG.encode(), shared_secret))}\n")
                else:
                    print(f"\nIntercepted message : {hex(proof(os.urandom(64), shared_secret))}\n")

        except Exception:
            print("System error.")
            sys.exit()


signal.alarm(360)
if __name__ == "__main__":
    challenge = Procyon()
    challenge.start()