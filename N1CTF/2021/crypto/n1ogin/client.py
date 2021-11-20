import os
import json
import time

from Crypto.PublicKey.RSA import import_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from pwn import *


PUB_KEY = import_key(open("n1ogin.pub", "r").read())


def seal(content):
    iv = os.urandom(16)
    aes_key = os.urandom(24)
    hmac_key = os.urandom(24)

    mm = int.from_bytes(PKCS1_pad(aes_key+hmac_key), 'big')
    rsa_data = pow(mm, PUB_KEY.e, PUB_KEY.n).to_bytes(2048//8, 'big')

    aes = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = aes.encryptor()
    cipher = encryptor.update(PKCS7_pad(content)) + encryptor.finalize()

    mac = iv + cipher
    for _ in range(7777):
        h = hmac.HMAC(hmac_key, hashes.MD5())
        h.update(mac)
        mac = h.finalize()
    aes_data = iv + cipher + mac

    res = {
        "rsa_data": rsa_data.hex(),
        "aes_data": aes_data.hex()
    }
    return res

def PKCS1_pad(payload):
    assert len(payload) == 48
    return b"\x00\x02" + b"\x77"*(2048//8-2-1-48) + b"\x00" + payload

def PKCS7_pad(payload):
    pad_length = 16 - len(payload)%16
    payload += bytes([pad_length]) * pad_length
    return payload

def login(conn):
    username = input("username: ")
    password = input("password: ")
    content = json.dumps({
        "choice": "login",
        "timestamp": int(time.time()),
        "nonce": os.urandom(8).hex(),
        "username": username,
        "password": password
    })
    envelope = json.dumps(seal(content.encode()))
    conn.sendlineafter(b"> ", envelope.encode())
    print(conn.recvline().decode())
    conn.interactive()

def register(conn):
    username = input("username: ")
    password = input("password: ")
    content = json.dumps({
        "choice": "register",
        "timestamp": int(time.time()),
        "nonce": os.urandom(8).hex(),
        "username": username,
        "password": password
    })
    envelope = json.dumps(seal(content.encode()))
    conn.sendlineafter(b"> ", envelope.encode())
    print(conn.recvline().decode())


def main():
    HOST = "127.0.0.1"
    PORT = 7777
    conn = remote(HOST, PORT)
    while True:
        choice = input("login/register: ")
        if choice == "login":
            login(conn)
        elif choice == "register":
            register(conn)
        else:
            break
    conn.close()

if __name__ == "__main__":
    main()