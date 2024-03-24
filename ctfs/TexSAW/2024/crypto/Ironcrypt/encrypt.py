from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
import sys

one = "----------------"
two = "----------------"
maxlen = 256

def encrypt(message, key):
    aes = AES.new(key, AES.MODE_OFB, two)
    return aes.encrypt(message)

def decrypt(message, key):
    aes = AES.new(key, AES.MODE_OFB, two)
    return aes.decrypt(message)

def decrypt_ecb(message, key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(message)

sys.stdout.write("Give me a message to encrypt:\n")
message = raw_input().strip()

msglen = len(message)
if msglen == 0:
    sys.stdout.write("No message provided.\n")
    sys.stdout.flush()
    quit()
elif msglen > maxlen:
    message = message[:maxlen]
elif msglen % 16 != 0:
    message += "0" * (16 - msglen % 16)

encrypted = encrypt(message, one)
sys.stdout.write("Original Message:  {}\n".format(message))
sys.stdout.write("Message in Hex:    {}\n".format(hexlify(message)))
sys.stdout.write("Encrypted Message: {}\n".format(hexlify(encrypted)))

sys.stdout.flush()
quit()

