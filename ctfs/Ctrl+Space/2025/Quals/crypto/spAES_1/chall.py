from spaes import spAES
import os
from base64 import b64encode, b64decode, binascii
from file_reader import read

intro = """Welcome to the super secure encryption service in-space!
    1) Encrypt text
    2) Obtain our super-secret file, you can't decrypt it!
    3) Quit"""

def main():
    secret_file = read('secret_file.txt')
    key = os.urandom(16)
    cipher = spAES(key)
    print(intro)
    for _ in range(2):
        answer = input("Your choice:")
        if answer == '1':
            try:
                pt = b64decode(input("Your text (base64):"))
                ct = cipher.encrypt_ecb(pt)
                print(b64encode(ct).decode())
            except binascii.Error:
                print("Invalid base64!")
        elif answer == '2':
            ct = cipher.encrypt_ecb(secret_file.encode())
            print(b64encode(ct).decode())
        elif answer == '3':
            break
        else:
            print("Unsupported operation!")
    print("Goodbye!")

if __name__ == '__main__':
    main()