#!/usr/bin/env python3

import os
import sys
import time
import struct
import subprocess
try:
    from Crypto.Cipher import AES
    from Crypto.Hash import HMAC, SHA256
except ImportError:
    print("PycryptoDome not installed.")
    sys.exit(1)

from secret import KEY
assert len(KEY) == 32

def decrypt_at_offset(data, offset, nonce):
    aes = AES.new(KEY, mode=AES.MODE_CTR, nonce=nonce)
    return aes.decrypt(b' ' * offset + data)[offset:]

def read_and_verify_packet():
    # read nonce
    nonce = sys.stdin.buffer.read(12)

    # read and decrypt length of tag
    tag_length = struct.unpack("<B", decrypt_at_offset(sys.stdin.buffer.read(1), 0, nonce))[0]

    # read and decrypt tag
    tag = decrypt_at_offset(sys.stdin.buffer.read(tag_length), 1, nonce)

    # read and decrypt length of data
    data_length = struct.unpack("<B", decrypt_at_offset(sys.stdin.buffer.read(1), tag_length + 1, nonce))[0]

    encrypted_data = sys.stdin.buffer.read(data_length)

    # verify encrypted data
    hmac = HMAC.new(KEY, msg=encrypted_data, digestmod=SHA256)
    try:
        hmac.verify(tag)
    except ValueError:
        print("Wrong MAC", flush=True)
        sys.exit(1)

    # decrypt and return data
    return decrypt_at_offset(encrypted_data, tag_length + 2, nonce)

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


while True:
    data = read_and_verify_packet()

    timestamp = struct.unpack("<I", data[:4])[0]
    data = data[4:]

    if (int(time.time()) - timestamp) < 10:
        try:
            output = subprocess.check_output(data, shell=True)

            sys.stdout.buffer.write(encrypt_packet(output))
            sys.stdout.buffer.flush()
        except:
            print("Something went wrong", flush=True)
            sys.exit(1)
    else:
        print("Packet too old", flush=True)
        sys.exit(1)