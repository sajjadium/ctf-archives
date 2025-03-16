#!/usr/local/bin/python

import random
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

MAX_ATTEMPTS = 1000

def encrypt_flag(flag):
    key = random.getrandbits(128).to_bytes(16, 'big')
    iv = random.getrandbits(128).to_bytes(16, 'big')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(flag.encode(), AES.block_size))
    return encrypted

def main():
    random.seed(time.time())
    encrypted_flag = encrypt_flag(open('./flag.txt').read())
    print("\n✨ Welcome to the **Guess the Number Challenge v1**! ✨")
    print("🕵️‍♂️ Can you uncover the secret behind the encrypted flag?")
    print("📜 Use your intelligence, strategy, and the hints provided to succeed!")

    print("Your task: Use your wits and strategy to uncover hints to decrypt the flag.")
    print(f"\nHere is your encrypted flag: \n{encrypted_flag.hex()}")
    print("\nBut don't worry, I'm generous. I've precomputed 1000 random hints for you!")
    print(f"You have {MAX_ATTEMPTS} attempts to guess the right index.\n")
    hints = [random.getrandbits(32) for _ in range(1000)]
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Attempt {attempt}/{MAX_ATTEMPTS}")
        try:
            index = int(input("Enter an index (0-999): ").strip())
            if 0 <= index < 1000:
                print(f"🔑 Hint at index {index}: {hints[index]}")
            else:
                print("❌ Invalid index! Please enter a number between 0 and 999.\n")
        except ValueError:
            print("❌ Invalid input! Please enter a valid integer.\n")
    print("\n✨ Your attempts are over! But don't give up just yet.")
    print("✨ Your attempts are over! Good luck solving the challenge!\n")
    print("🔍 Don't forget: The key to solving the challenge lies in these random hints. Goodbye!")

if __name__ == "__main__":
    main()
