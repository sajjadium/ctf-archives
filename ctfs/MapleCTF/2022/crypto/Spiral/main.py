from spiral import Spiral
from secret import flag
from os import urandom

menu = """Options:
1. Get encrypted flag
2. Encrypt message"""
key = urandom(16)
cipher = Spiral(key, rounds=4)


def main():
    print(menu)
    while True:
        try:
            option = int(input(">>> "))
            if option == 1:
                ciphertext = cipher.encrypt(flag)
                print(ciphertext.hex())
            elif option == 2:
                plaintext = bytes.fromhex(input())
                ciphertext = cipher.encrypt(plaintext)
                print(ciphertext.hex())
            else:
                print("Please select a valid option")

        except Exception:
            print("Something went wrong, please try again.")


if __name__ == "__main__":
    main()
