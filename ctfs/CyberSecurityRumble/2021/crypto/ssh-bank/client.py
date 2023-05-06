import os
import sys
import time
import struct
from pwn import *
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256

KEY = b'[redacted]'
packet = b''

r = remote('challs.rumble.host', 6382)

def read_and_verify_packet():
    global packet
    nonce = r.recvn(12)
    packet += nonce

    aes = AES.new(KEY, mode=AES.MODE_CTR, nonce=nonce)
    encrypted_length = r.recvn(1)
    packet += encrypted_length
    tag_length = struct.unpack("<B", aes.decrypt(encrypted_length))[0]

    aes = AES.new(KEY, mode=AES.MODE_CTR, nonce=nonce)
    encrypted_tag = r.recvn(tag_length)
    packet += encrypted_tag
    tag = aes.decrypt(b' ' + encrypted_tag)[1:]

    aes = AES.new(KEY, mode=AES.MODE_CTR, nonce=nonce)
    encrypted_length = r.recvn(1)
    packet += encrypted_length
    data_length = struct.unpack("<B", aes.decrypt(b' ' * (tag_length + 1) + encrypted_length)[-1:])[0]

    encrypted_data = r.recvn(data_length)
    packet += encrypted_data

    hmac = HMAC.new(KEY, msg=encrypted_data, digestmod=SHA256)
    try:
        hmac.verify(tag)
    except ValueError:
        print("Wrong MAC", flush=True)
        sys.exit(1)

    aes = AES.new(KEY, mode=AES.MODE_CTR, nonce=nonce)
    return aes.decrypt(b' ' * (tag_length + 2) + encrypted_data)[tag_length + 2:]

def encrypt_packet(data):
    data = struct.pack("<I", int(time.time())) + data
 
    hmac = HMAC.new(KEY, digestmod=SHA256)

    nonce = os.urandom(12)
    aes = AES.new(KEY, mode=AES.MODE_CTR, nonce=nonce)

    payload = aes.encrypt(b' ' * (hmac.digest_size + 2) + data)[hmac.digest_size + 2:]

    hmac.update(payload)
    tag = hmac.digest()

    aes = AES.new(KEY, mode=AES.MODE_CTR, nonce=nonce)
    payload = aes.encrypt(struct.pack("<B", len(tag)) + tag + struct.pack("<B", len(data)) + data)

    return nonce + payload

r.send(encrypt_packet(b'cat /app/flag.txt'))
print(read_and_verify_packet()[4:])
