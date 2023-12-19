#!/usr/bin/python3 -u
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from secret import FLAG

TOKEN = ''.join(['{:02x}'.format(byte) for byte in os.urandom(9)])

def get_tokens():
    tokens = [str(TOKEN[i:i+3]) for i in range(0, len(TOKEN), 3)]
    return tokens

def derive_key(token, iterations=100000, key_length=32):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'CryPT0N1t3',
        length=key_length,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(token.encode())
    return key

def decrypt(ciphertext, token_index):
    nonce = ciphertext[:12]
    ciphertext = ciphertext[12:]
    key = derive_key(tokens[token_index])
    cipher = ChaCha20Poly1305(key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    return plaintext

def main():
    global tokens
    global token_index
    global queries

    tokens = get_tokens()
    token_index = 0
    queries = 0

    while queries <= 800:
        print ("\nchoose an option:\n")
        print("1. select token")
        print("2. decrypt")
        print("3. get flag")
        print("4. exit")

        option = input(">>: ")

        if option == "1":
            sel = int(input("\nselect a token (1-6)\n>>: "))
            if 1 <= sel <= 6:
                token_index = sel - 1
            else:
                print("invalid token index")

        elif option == "2":
            ciphertext = bytes.fromhex(input("ciphertext (hex): "))
            try:
                pt = decrypt(ciphertext, token_index)
                print (f"decrypted (hex): {pt.hex()}")
            except:
                print ("error decrypting")

        elif option == "3":
            entered_token = input("enter token: ")
            if entered_token == TOKEN:
                print(f"{FLAG}")
                break
            else:
                print("wrong token")
                break

        elif option == "4":
            break

        queries += 1

if __name__ == "__main__":
    main()
