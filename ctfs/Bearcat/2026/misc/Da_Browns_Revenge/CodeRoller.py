#!/usr/local/bin/python3 -u
import random

def generate_12bit_code():
    """Generate a random 12-bit code as a binary string."""
    return format(random.getrandbits(12), '012b')

def main():
    loginnumber = 0
    while loginnumber < 20:
        code = generate_12bit_code()

        user_input = input("Enter the access string: ").strip()
        if len(user_input) > 4107:
            print("Access Denied - Character limit 4107")
            break
        elif not set(user_input) <= {'1', '0'}:
            print("Access Denied - Passcode may only contain 0s and 1s")
            break
        else:
            if code in user_input:
                loginnumber += 1
                print(f"Correct Access Code, {loginnumber} out of 20")
            else:
                print("Access Denied - Passcode not Found")
                break
    else:
        with open("flag.txt", "r") as file:
            contents = file.read()
            print(contents)

if __name__ == "__main__":
    main()
