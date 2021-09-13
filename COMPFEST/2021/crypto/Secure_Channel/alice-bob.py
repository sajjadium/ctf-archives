#!/usr/bin/env python3
import sys
from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime, bytes_to_long  as bl, long_to_bytes as lb
from secrets import Alice, Bob
from chats import alice_dialogue, bob_dialogue
import time

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

try:
    g = bl(b64decode(input('g: ')))
    assert g > 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    p = getPrime(512)

    alice = Alice()
    bob = Bob()

    alice_public_part = alice.make_public_part(g, p)
    bob_public_part = bob.make_public_part(g, p)

    alice.make_private_part(bob_public_part, p)
    bob.make_private_part(alice_public_part, p)

    print('p:', p)
    print('Alice\'s public part:', b64encode(lb(alice_public_part)).decode())
    #print('Bob\'s public part:', b64encode(lb(bob_public_part)).decode()) # Bob doesn't want to share it to you :(
    print()

    assert len(alice_dialogue) == len(bob_dialogue)
    while True:        
        for i in range(len(alice_dialogue)):
            print('Messages from Alice:')
            msg = alice.send_message(alice_dialogue[i])
            print(b64encode(msg).decode())
            print(bob.receive_message(msg))
            print()
            time.sleep(0.5)

            print('Messages from Bob:')    
            msg = bob.send_message(bob_dialogue[i])
            print(b64encode(msg).decode())
            print(alice.receive_message(msg))
            print()
            time.sleep(0.5)
except:
    print('Something is wrong.')
    exit(0)