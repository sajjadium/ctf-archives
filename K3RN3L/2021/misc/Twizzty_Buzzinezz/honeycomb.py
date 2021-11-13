#!/usr/bin/env python3
#
# Polymero
#

# Imports
import os

FLAG = b'flag{...REDACTED...}'

class HoneyComb:
    def __init__(self, key):
        self.vals = [i for i in key]
        
    def turn(self):
        self.vals = [self.vals[-1]] + self.vals[:-1]
        
    def encrypt(self, msg):
        keystream = []
        while len(keystream) < len(msg):
            keystream += self.vals
            self.turn()
        return bytes([msg[i] ^ keystream[i] for i in range(len(msg))]).hex()

hc = HoneyComb(os.urandom(6))

print(hc.encrypt(FLAG))
