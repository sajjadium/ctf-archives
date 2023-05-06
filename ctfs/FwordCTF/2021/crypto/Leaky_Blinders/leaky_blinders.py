#!/usr/bin/env python3.8
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sys, os
                  
FLAG = b"FwordCTF{###############################################################}"

WELCOME = '''
Welcome to Enc/Dec Oracle.
'''

key = os.urandom(32)

def xor(a, b):
    return bytearray([a[i % len(a)] ^ b[i % len(b)] for i in range(max(len(a), len(b)))])

def encrypt(msg):
    aes = AES.new(key, AES.MODE_ECB)
    if len(msg) % 16 != 0:
        msg = pad(msg, 16)
    cipher = aes.encrypt(msg)
    cipher = xor(cipher, key)
    return cipher

def decrypt(cipher, k):
    aes = AES.new(k, AES.MODE_ECB)
    cipher = xor(cipher, k)
    msg = unpad(aes.decrypt(cipher), 16)
    return msg


class Leaky_Blinders:
    def __init__(self):
        print(WELCOME + f"Here is the encrypted flag : {encrypt(FLAG).hex()}")

    def start(self):
        try:
            while True:
                print("\n1- Encrypt")
                print("2- Decrypt")
                print("3- Leave")
                c = input("> ")

                if c == '1':
                    msg = os.urandom(32)
                    cipher = encrypt(msg)
                    if all(a != b for a, b in zip(cipher, key)):
                        print(cipher.hex())
                    else:
                        print("Something seems leaked !")

                elif c == '2':
                    k = bytes.fromhex(input("\nKey : "))
                    cipher = bytes.fromhex(input("Ciphertext : "))
                    flag = decrypt(cipher, k)
                    if b"FwordCTF" in flag:
                        print(f"Well done ! Here is your flag : {FLAG}")
                    else:
                        sys.exit("Wrong key.")

                elif c == '3':
                    sys.exit("Goodbye :)")

        except Exception:
          sys.exit("System error.")


if __name__ == "__main__":
    challenge = Leaky_Blinders()
    challenge.start()