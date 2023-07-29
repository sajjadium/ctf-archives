from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = b"redacted" * 2

FLAG = "redacted"

initial_cipher = bytes.fromhex(input("Initial HEX: ").strip())

cipher = AES.new(KEY, AES.MODE_ECB).encrypt(pad(initial_cipher, 16))
print(cipher.hex())
cipher = AES.new(KEY, AES.MODE_ECB).encrypt(pad(cipher, 16))
print(cipher.hex())

cipher = AES.new(KEY, AES.MODE_ECB).encrypt(pad(cipher, 16))
result = bytes.fromhex(input("Result HEX: ").strip())

if cipher == result:
    print(FLAG)
else:
    print("Not quite...")