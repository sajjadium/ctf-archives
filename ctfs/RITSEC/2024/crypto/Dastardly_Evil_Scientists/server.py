from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from secret import KEY, FLAG

BLOCK_SIZE = 64

key = bytes.fromhex(KEY)
cipher = DES.new(key, DES.MODE_ECB)
flag = cipher.encrypt(pad(bytes(FLAG, "utf-8"), BLOCK_SIZE))

print("Here's the flag (in hex):", flag.hex())
print("=" * 64)
print("Encrypt something if you want, you can choose the key and the plaintext :)")
while True:
    try:
        key = bytes.fromhex(input("Key (in hex): "))
        plaintext = bytes.fromhex(input("Message to encrypt (in hex): "))
        print("=" * 64)
        cipher = DES.new(key, DES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))
        print("Here's your message! (in hex):", ciphertext.hex())
        print("Here's your message! (in bytes):", ciphertext)
        print("=" * 64)
    except KeyboardInterrupt:
        break

