#!/usr/local/bin/python -u

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import random
from time import time

key = get_random_bytes(16)
flag = open('flag.txt', 'rb').read().strip()


def pad(msg, block_size):
    random.seed(seed)
    p = b''
    pad_len = block_size - (len(msg) % block_size)
    while len(p) < pad_len:
        b = bytes([random.randrange(256)])
        if b not in p:
            p += b

    return msg + p


def unpad(msg, block_size):
    random.seed(seed)
    p = b''
    while len(p) < block_size:
        b = bytes([random.randrange(256)])
        if b not in p:
            p += b

    if p[0] not in msg:
        raise ValueError('Bad padding')

    pad_start = msg.rindex(p[0])
    if msg[pad_start:] != p[:len(msg) - pad_start]:
        raise ValueError('Bad padding')

    return msg[:pad_start]


def encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct


def decrypt(data):
    iv = data[:AES.block_size]
    ct = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ct), AES.block_size)


print('Hi! Welcome to our oracle, now extra secure because of our custom padding!')
seed = int(time() // 10)
print('We have this really cool secret here: ' + encrypt(flag).hex())


while True:
    try:
        decrypt(bytes.fromhex(input("Ciphertext: ")))
        print("ok")
    except:
        print("error!!!")
    print()
