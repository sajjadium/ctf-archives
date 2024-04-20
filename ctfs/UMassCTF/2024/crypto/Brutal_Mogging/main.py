import os
from hashlib import sha256

from flag import FLAG

def xor(data1, data2):
    return bytes([data1[i] ^ data2[i] for i in range(len(data1))])

def do_round(data, key):
    m = sha256()
    m.update(xor(data[2:4], key))
    return bytes(data[2:4]) + xor(m.digest()[0:2], data[0:2])

def do_round_inv(data, key):
    m = sha256()
    m.update(xor(data[0:2], key))
    return xor(m.digest()[0:2], data[2:4]) + bytes(data[0:2])

def pad(data):
    padding_length = 4 - (len(data) % 4)
    return data + bytes([padding_length] * padding_length)

def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

# XOR every character with bytes generated from the PRNG
def encrypt_block(data, key):
    
    for i in range(10):
        data = do_round(data, key)
    return data

def decrypt_block(data, key):
    for i in range(10):
        data = do_round_inv(data, key)
    return data

def encrypt_data(data, key):
    cipher = b''
    while data:
        cipher += encrypt_block(data[:4], key)
        data = data[4:]
    return cipher

def decrypt_data(cipher, key):
    data = b''
    while cipher:
        data += decrypt_block(cipher[:4], key)
        cipher = cipher[4:]
    return data

def encrypt(data, key):
    data = pad(data)
    return encrypt_data(encrypt_data(data, key[0:2]), key[2:4])

def decrypt(data, key):
    plain = decrypt_data(decrypt_data(data, key[2:4]), key[0:2])
    return unpad(plain)

if __name__ == '__main__':
    key = os.urandom(4)
    cipher = encrypt(FLAG, key)

    print("Oh yeah, my cipher is so strong and my one way function is so well defined.")
    print("No betas can ever break it, so I'll just give you the flag right now.")

    print(f"The encrypted flag is: {cipher.hex()}")

    print("I need to get back to looksmaxxing so I'll give you three small pieces of advice.")
    print("What are your questions?")
    for i in range(3):
        plain = input(f"{i}: ")[0:8]
        cipher = encrypt(plain.encode(), key)
        print(f"{plain}: {cipher.hex()}")