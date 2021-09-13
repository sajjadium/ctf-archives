#!/usr/bin/env python3
import sys
from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime, bytes_to_long  as bl, long_to_bytes as lb
from secrets import Alice, You

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
    your_secret = bl(b64decode(input('Your secret: ')))
    g = bl(b64decode(input('g: ')))
    assert g > 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    p = getPrime(512)

    alice = Alice()
    you = You(your_secret)

    alice_public_part = alice.make_public_part(g, p)
    your_public_part = you.make_public_part(g, p)

    alice.make_private_part(your_public_part, p)
    your_private_part = you.make_private_part(alice_public_part, p)

    print('p:', p)
    print('Alice\'s public part:', b64encode(lb(alice_public_part)).decode())
    print('Your public part:', b64encode(lb(your_public_part)).decode())
    print('Your private part:', b64encode(your_private_part).decode())
    print()

    while True:
        msg = b64decode(input('Message to Alice: '))
        print(alice.receive_message(msg))
        print()

except:
    print('Something is wrong.')
    exit(0)