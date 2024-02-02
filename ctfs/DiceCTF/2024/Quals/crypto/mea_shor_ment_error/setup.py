from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

nbits = 3072
key = RSA.generate(nbits)
with open("flag.txt", "rb") as f:
    flag = f.read()
cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(flag)

with open("privatekey.pem", "wb") as f:
    data = key.export_key()
    f.write(data)
with open("publickey.pem", "wb") as f:
    data = key.public_key().export_key()
    f.write(data)
with open("ciphertext.bin", "wb") as f:
    f.write(ciphertext)