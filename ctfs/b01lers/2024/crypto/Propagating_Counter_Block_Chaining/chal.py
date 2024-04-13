from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from functools import reduce
from secret import flag
import os
import json

BLOCK_SIZE = 16
key_ctr1 = os.urandom(BLOCK_SIZE)
key_ctr2 = os.urandom(BLOCK_SIZE)
key_cbc = os.urandom(BLOCK_SIZE)
nonce1 = os.urandom(8)
nonce2 = os.urandom(8)

def AES_ECB_enc(key, message):
    enc = AES.new(key, AES.MODE_ECB)
    return enc.encrypt(message)

def AES_ECB_dec(key, message):
    enc = AES.new(key, AES.MODE_ECB)
    return enc.decrypt(message)

# Returning a block each time
def get_blocks(message):
    for i in range(0, len(message), BLOCK_SIZE):
        yield message[i:i+BLOCK_SIZE]
    return

# Takes any number of arguements, and return the xor result.
# Similar to pwntools' xor, but trucated to minimum length
def xor(*args):
    _xor = lambda x1, x2: x1^x2
    return bytes(map(lambda x: reduce(_xor, x, 0), zip(*args)))


def counter(nonce):
    count = 0
    while count < 2**(16 - len(nonce)):
        yield nonce + str(count).encode().rjust(16-len(nonce), b"\x00")
        count+=1
    return


def encrypt(message):
    cipher = b""
    iv = os.urandom(BLOCK_SIZE)
    prev_block = iv
    counter1 = counter(nonce1)
    counter2 = counter(nonce2)
    for block in get_blocks(pad(message, BLOCK_SIZE)):
        enc1 = AES_ECB_enc(key_ctr1, next(counter1))
        enc2 = AES_ECB_enc(key_cbc, xor(block, prev_block, enc1))
        enc3 = AES_ECB_enc(key_ctr2, next(counter2))
        enc4 = xor(enc3, enc2)
        prev_block = xor(block, enc4)
        cipher += enc4

    return iv + cipher

def decrypt(cipher):
    message = b""
    iv = cipher[:16]
    cipher_text = cipher[16:]

    prev_block = iv
    counter1 = counter(nonce1)
    counter2 = counter(nonce2)
    for block in get_blocks(cipher_text):
        dec1 = AES_ECB_enc(key_ctr2, next(counter2))
        dec2 = AES_ECB_dec(key_cbc, xor(block, dec1))
        dec3 = AES_ECB_enc(key_ctr1, next(counter1))
        message += xor(prev_block, dec2, dec3)
        prev_block = xor(prev_block, dec2, block, dec3)

    return unpad(message, BLOCK_SIZE)

def main():
    certificate = os.urandom(8) + flag + os.urandom(8)
    print(f"""
*********************************************************

Certificate as a Service

*********************************************************

Here is a valid certificate: {encrypt(certificate).hex()}

*********************************************************""")
    while True:
        try:
            cert = bytes.fromhex(input("Give me a certificate >> "))
            if len(cert) < 32:
                print("Your certificate is not long enough")

            message = decrypt(cert)
            if flag in message:
                print("This certificate is valid")
            else:
                print("This certificate is not valid")
        except Exception:
            print("Something went wrong")
            
if __name__ == "__main__":
    main()

