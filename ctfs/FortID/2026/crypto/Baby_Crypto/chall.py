#!/usr/bin/python3

import json
import signal
import sys

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from secret import FLAG


BANNER = """
   _____                              _    __            ____
  / ___/___  _______  __________     | |  / /___ ___  __/ / /_
  \\__ \\/ _ \\/ ___/ / / / ___/ _ \\    | | / / __ `/ / / / / __/
 ___/ /  __/ /__/ /_/ / /  /  __/    | |/ / /_/ / /_/ / / /_
/____/\\___/\\___/\\__,_/_/   \\___/     |___/\\__,_/\\__,_/_/\\__/
"""


MENU = """
Options:
  1) Safely Store a Secret Value
  2) Export Vault Data
  3) Exit

"""

class Cipher:
    def __init__(self):
        self.key = get_random_bytes(16)


    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=plaintext[:8])
        return cipher.encrypt(plaintext)


class Vault:
    def __init__(self):
        self.cipher = Cipher()
        self.entries = {}


    def insert(self, secret_value):
        ciphertext = self.cipher.encrypt(secret_value.encode("utf-8"))
        self.entries[f"Secret #{len(self.entries)}"] = ciphertext.hex()


    def export(self):
        return json.dumps(self.entries)


def timeout_handler(signum, frame):
    print("Timeout!")
    sys.exit(1)


def main():
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(15)

    assert FLAG.startswith("FortID{") and FLAG.endswith("}")

    print(BANNER)

    vault = Vault()
    vault.insert(FLAG)

    print(MENU)

    while True:
        user_input = input("> ").strip()

        if user_input not in ["1", "2", "3"]:
            print("Are you ok?")
            continue

        if int(user_input) == 1:
            user_secret = input("Enter secret: ").strip()
            vault.insert(user_secret)
        elif int(user_input) == 2:
            print(vault.export())
        else:
            break



if __name__ == '__main__':
    main()
