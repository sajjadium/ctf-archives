from spaes import spAES
import os
from base64 import b64encode, b64decode, binascii

flag = os.getenv("FLAG", "space{fake}")

intro = """Welcome to the super secure encryption service in-space!
    1) Encrypt text
    2) Guess the key!
    3) Quit"""

def main():
    key = os.urandom(16)
    print(intro)
    while True:
        answer = input("Your choice:")
        if answer == '1':
            try:
                pt = b64decode(input("Your text (base64):"))
                tweak = b64decode(input("Your tweak (base64):"))
                assert len(tweak) == 16, "Invalid tweak length!"
                cipher = spAES(key, tweak)
                ct = cipher.encrypt_ecb(pt)
                print(b64encode(ct).decode())
            except binascii.Error:
                print("Invalid base64!")
        elif answer == '2':
            key_guess = b64decode(input("Key (base64):"))
            if key_guess == key:
                print(flag)
        elif answer == '3':
            break
        else:
            print("Unsupported operation!")
    print("Goodbye!")

if __name__ == '__main__':
    main()