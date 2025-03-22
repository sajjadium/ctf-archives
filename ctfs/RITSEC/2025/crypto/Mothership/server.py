import base64
import os
import signal

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

COORDS = open("coordinates.txt").read().strip()


def encrypt(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(message.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return base64.b64encode(iv + ciphertext).decode()


def validate(data, key):
    try:
        data = base64.b64decode(data)
        iv = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

        return decrypted == "SHIP:FIRE"
    except:
        print("Invalid transmission.")
        raise SystemExit(1)


def main():
    print("=== Alien Transmission System ===")
    print("Welcome to the transmission system.")

    signal.alarm(11)
    for i in range(200):
        key = os.urandom(16)
        iv = os.urandom(16)

        print("\nSAFE TRANSMISSION:", encrypt("SHIP:SAFE", key, iv))
        data = input("SEND TRANSMISSION: ")
        if not validate(data, key):
            print("Safe transmission received. Exiting.")
            return
        print(f"Attack transmission received ({i + 1}/200). Continue to confirm.")

    print("Attack mode initiated. Ship coordinates:", COORDS)


if __name__ == "__main__":
    main()
