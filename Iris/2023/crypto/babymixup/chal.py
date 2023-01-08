from Crypto.Cipher import AES
import os

key = os.urandom(16)

flag = b"flag{REDACTED}"
assert len(flag) % 16 == 0

iv = os.urandom(16)
cipher = AES.new(iv,  AES.MODE_CBC, key)
print("IV1 =", iv.hex())
print("CT1 =", cipher.encrypt(b"Hello, this is a public message. This message contains no flags.").hex())

iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv )
print("IV2 =", iv.hex())
print("CT2 =", cipher.encrypt(flag).hex())
