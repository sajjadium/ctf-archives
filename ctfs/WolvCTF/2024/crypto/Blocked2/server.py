
import random
import secrets
import sys
import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor


MASTER_KEY = secrets.token_bytes(16)


def encrypt(message):
    if len(message) % 16 != 0:
        print("message must be a multiple of 16 bytes long! don't forget to use the WOLPHV propietary padding scheme")
        return None

    iv = secrets.token_bytes(16)
    cipher = AES.new(MASTER_KEY, AES.MODE_ECB)
    blocks = [message[i:i+16] for i in range(0, len(message), 16)]

    # encrypt all the blocks
    encrypted = [cipher.encrypt(b) for b in [iv, *blocks]]

    # xor with the next block of plaintext
    for i in range(len(encrypted) - 1):
        encrypted[i] = strxor(encrypted[i], blocks[i])

    return iv + b''.join(encrypted)


def main():
    message = open('message.txt', 'rb').read()

    print("""                 __      __
 _      ______  / /___  / /_ _   __
| | /| / / __ \\/ / __ \\/ __ \\ | / /
| |/ |/ / /_/ / / /_/ / / / / |/ /
|__/|__/\\____/_/ .___/_/ /_/|___/
              /_/""")
    print("[          email portal          ]")
    print("you are logged in as doubledelete@wolp.hv")
    print("")
    print("you have one new encrypted message:")
    print(encrypt(message).hex())

    while True:
        print(" enter a message to send to dree@wolp.hv, in hex")
        s = input(" > ")
        message = bytes.fromhex(s)
        print(encrypt(message).hex())


main()
