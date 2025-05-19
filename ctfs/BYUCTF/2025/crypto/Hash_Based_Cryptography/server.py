#!/usr/local/bin/python

import hashlib
from secrets import KEY, FLAG

def gen_otp(key: bytes, message: bytes) -> bytes:
    iv = key
    otp = b''
    for _ in range(len(message)//20):
        iv = hashlib.sha1(iv).digest()
        otp += iv
    return otp

def pad(message):
    if type(message) is str:
        message = message.encode()
    return message + bytes([(20 - len(message)) % 20]) * ((20 - len(message)) % 20)

def unpad(message):
    if message[-1] > 20 or message[-1] != message[-message[-1]]:
        print("Padding error")
        raise ValueError("Invalid padding")
    return message[:-message[-1]]

def encrypt(key, message) -> str:
    if type(key) is str:
        key = key.encode()
    return bytes([a^b for a, b in zip(pad(message), gen_otp(key, pad(message)))]).hex()

def decrypt(key, message) -> str:
    if type(key) is str:
        key = key.encode()
    try:
        message = bytes.fromhex(message)
        return unpad(bytes([a^b for a, b in zip(message, gen_otp(key, pad(message)))])).decode(errors='ignore')
    except Exception as e:
        return f"Error decrypting"

def test():
    print(encrypt("key", "hello world"))
    print(decrypt("key", "ce4a4e49d050c8c3b9ab95e62330713f787a7ed7"))

def main():
    print("I just created this encryption system. I think it's pretty cool")
    print("Here's the encrypted flag:")
    print(encrypt(KEY, FLAG))
    print("Here, you can try it out, too:")
    while True:
        user_input = input(" > ")
        decrypted = decrypt(KEY, user_input)
        if FLAG in decrypted or "byuctf" in decrypted:
            print("I didn't make it that easy")
            continue
        print(decrypted.encode())

if __name__ == "__main__":
    main()