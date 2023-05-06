import base64
import hashlib
import os
import sys
from datetime import datetime

from Crypto.Cipher import AES


def encrypt(data, key, iv):
    encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
    return encryptor.encrypt(data)


def pad(data):
    missing = 16 - len(data) % 16
    return data + (chr(missing) * missing).encode()


def printout(msg):
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


def main():
    flag = open("flag.txt", "rb").read()
    assert len(flag) == 16
    timestamp = str(datetime.now())
    IV = hashlib.md5(timestamp.encode('ascii')).digest()
    key = os.urandom(16)
    printout(timestamp)
    printout("Hello to FIEND encryption service!")
    try:
        while True:
            printout("Give me message (base64 encoded):")
            msg = input()
            msg = base64.b64decode(msg) + flag
            plaintext = pad(msg)
            ciphertext = encrypt(plaintext, key, IV)
            printout(base64.b64encode(ciphertext).decode("ascii"))
            IV = hashlib.md5(IV).digest()
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        printout("Phail :(")
    pass


main()
