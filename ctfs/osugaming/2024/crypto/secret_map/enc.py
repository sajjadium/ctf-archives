import os

xor_key = os.urandom(16)

with open("flag.osu", 'rb') as f:
    plaintext = f.read()

encrypted_data = bytes([plaintext[i] ^ xor_key[i % len(xor_key)] for i in range(len(plaintext))])

with open("flag.osu.enc", 'wb') as f:
    f.write(encrypted_data)
