#!/usr/local/bin/python

import os
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

MAX_ATTEMPTS = 10

def encrypt_flag(flag, iv):
    key = random.getrandbits(128).to_bytes(16, 'big')
    cipher = AES.new(key, AES.MODE_CBC, iv*2)
    encrypted = cipher.encrypt(pad(flag.encode(), AES.block_size))
    return encrypted

def main():
    secureSeed = os.urandom(8)
    random.seed(secureSeed)
    hints = [random.getrandbits(32) for _ in range(624)]
    encrypted_flag = encrypt_flag(open('./flag.txt').read(), secureSeed)

    print("\n✨ Welcome to the **Guess the Number Challenge v2**! ✨")
    print("🕵️‍♂️ Your mission: Decode the encrypted flag by uncovering critical hints.")
    print("📊 We've precomputed 624 random numbers using a secure PRNG.")
    print(f"❗ But there's a catch: You can only access {MAX_ATTEMPTS} of them.")
    print("🔑 Choose your indices wisely to uncover the key!")
    print("\n📜 Instructions:")
    print("1️⃣ You have 624 unique random numbers that are critical for decrypting the flag.")
    print("2️⃣ Enter an index (0-623) to reveal a hint.")
    print(f"3️⃣ You only have {MAX_ATTEMPTS} attempts, so choose wisely!")
    print("4️⃣ Use your understanding of randomness to crack the secure seed.")

    print(f"\n🔒 Here is your encrypted flag: \n{encrypted_flag.hex()}")
    print(f"\nGood luck! You have {MAX_ATTEMPTS} attempts to guess the correct index.\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Attempt {attempt}/{MAX_ATTEMPTS}")
        try:
            index = int(input("Enter an index (0-624): ").strip())
            if 0 <= index < 624:
                print(f"Hint at index {index}: {hints[index]}\n")
            else:
                print("❌ Invalid index! Please enter a number between 0 and 624.\n")
        except ValueError:
            print("❌ Invalid input! Please enter a valid integer.\n")
    print("✨ Your attempts are over! Good luck solving the challenge!\n")
    print("🔍 Remember, the flag is encrypted. Use your hints wisely. Goodbye!")

if __name__ == "__main__":
    main()
