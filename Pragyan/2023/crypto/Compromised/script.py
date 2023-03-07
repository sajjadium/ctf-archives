#!/usr/local/bin/python

from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from hashlib import sha256
from random import randrange
from os import urandom
import sys

def is_too_much_evil(x, y):
    if y <= 0:
        return True
    z = x//y
    while z&1 == 0:
        z >>= 1
    return z == 1

def magic(key):
    flag = open("flag.txt", 'rb').readline()
    key = sha256(long_to_bytes(key)).digest()
    iv = urandom(AES.block_size)
    aes = AES.new(key, AES.MODE_CBC, iv)
    ct = iv + aes.encrypt(pad(flag, AES.block_size))
    return ct

p = 143631585913210514235039010914091901837885309376633126253342809551771176885137171094877459999188913342142748419620501172236669295062606053914284568348811271223549440680905140640909882790482660545326407684050654315851945053611416821020364550956522567974906505478346737880716863798325607222759444397302795988689
g = 65537
o = p-1

try:
    eve = int(input('Eve\'s evil number: '), 16)
    if is_too_much_evil(o, eve):
        raise Exception
except:
    sys.exit(1)

alice_secret = randrange(2, o)
recv_alice = pow(g, alice_secret, p)
print('Received from Alice:', hex(recv_alice)[2:])

send_bob = pow(recv_alice, eve, p)
print('Sent to Bob:', hex(send_bob)[2:])

bob_scret = randrange(2, o)
recv_bob = pow(g, bob_scret, p)
print('Received from Bob:', hex(recv_bob)[2:])

send_alice = pow(recv_bob, eve, p)
print('Sent to Alice:', hex(send_alice)[2:])

key = pow(send_alice, alice_secret, p)
if key != pow(send_bob, bob_scret, p):
    sys.exit(1)

print('Ciphertext:', magic(key).hex())
