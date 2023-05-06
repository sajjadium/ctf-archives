import os
import random

from Crypto.Cipher import AES

KEY = os.urandom(16)
PASSWORD = os.urandom(16)
FLAG = os.getenv('FLAG')

menu = """========================
1. Access Flag
2. Change Password
========================"""


def xor(byte, bytes_second):
    d = b''
    for i in range(len(bytes_second)):
        d += bytes([byte ^ bytes_second[i]])
    return d


def decrypt(ciphertext):
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = AES.new(KEY, AES.MODE_ECB)
    pt = b''
    state = iv
    for i in range(len(ct)):
        b = cipher.encrypt(state)[0]
        c = b ^ ct[i]
        pt += bytes([c])
        state = state[1:] + bytes([ct[i]])
    return pt


if __name__ == "__main__":
    while True:
        print(menu)
        option = int(input("> "))
        if option == 1:
            password = bytes.fromhex(input("Password > "))
            if password == PASSWORD:
                print(FLAG)
                exit(0)
            else:
                print("Wrong password!")
                continue
        elif option == 2:
            token = input("Token > ")
            if len(token) != 64:
                print("Wrong length!")
                continue
            hex_token = bytes.fromhex(token)
            r_byte = random.randbytes(1)
            print(f"XORing with: {r_byte.hex()}")
            xorred = xor(r_byte[0], hex_token)
            PASSWORD = decrypt(xorred)
