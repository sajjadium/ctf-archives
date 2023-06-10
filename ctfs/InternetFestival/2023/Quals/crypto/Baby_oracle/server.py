#!/usr/bin/env python3

import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import sys

null = open(os.devnull, 'w')
sys.stderr = null

FLAG = os.environ.get("FLAG")
key = os.urandom(16)


def encrypt(message: object) -> bytes:
    msg = pickle.dumps(message)
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(msg, cipher.block_size))
    return cipher.iv + cipher_text


def decrypt(cipher_text: bytes) -> object:
    iv = cipher_text[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = cipher.decrypt(cipher_text[16:])
    # no padding oracle
    # msg = unpad(msg)
    return pickle.loads(msg)

QUESTIONS = ["name", "surname", "age", "email", "phone", "address", "city", "country"]

def main():

    print("Welcome, the service is currently in beta, just three options available:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    
    while True:
        choice = input("What do you want to do? [1,2,3]: ")
        if choice == "1":
            responses = []
            for question in QUESTIONS:
                response = input(f"What's your {question}? ")
                if len(response) < 4 or len(response) > 32:
                    print("Invalid response")
                    exit(0)
                responses.append(response)

            token = encrypt((*responses, False))
            print(f"Here is your login token: {token.hex()}")
            
        elif choice == "2":
            token = bytes.fromhex(input("Send your token: "))
            try:
                name, _, _, _, _, _, _, _, is_admin = decrypt(token)
                if is_admin:
                    print(f"Welcome {name}, here is your flag: {FLAG}")
                else:
                    print(f"Welcome {name}")
            except Exception as e:
                print("Invalid token")

        elif choice == "3":
            print("Bye")
            exit(0)
            
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()