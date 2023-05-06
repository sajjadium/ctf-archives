#!/usr/bin/env python3
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256, HMAC, BLAKE2s
from Crypto.Random import urandom, random
from secret import FLAG, PASSWORD

encryption_key = BLAKE2s.new(data=PASSWORD + b'encryption_key').digest()
mac_key = BLAKE2s.new(data=PASSWORD + b'mac_key').digest()

def int_to_bytes(i):
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')

def encode(s):
    bits = bin(int.from_bytes(s, byteorder='big'))[2:]
    ret = ''
    
    for bit in bits:
        if bit == '1':
            if random.randrange(0,2):
                ret += '01'
            else:
                ret += '10'
        else:
            ret += '00'
    
    return int_to_bytes(int(ret, base=2))

def decode(s):
    bits = bin(int.from_bytes(s, byteorder='big'))[2:]
    if len(bits) % 2:
        bits = '0' + bits

    ret = ''

    for i in range(0,len(bits)-1,2):
        if int(bits[i] + bits[i+1],base=2):
            ret += '1'
        else:
            ret += '0'

    return int_to_bytes(int(ret, base=2))

def encrypt(m):
    nonce = urandom(8)

    aes = AES.new(key=encryption_key, mode=AES.MODE_CTR,nonce=nonce)
    tag = HMAC.new(key=mac_key, msg=m).digest()

    return nonce + aes.encrypt(encode(m) + tag)

def decrypt(c):
    try:
        aes = AES.new(key=encryption_key, mode=AES.MODE_CTR,nonce=c[:8])
        
        decrypted = aes.decrypt(c[8:])
        message, tag = decode(decrypted[:-16]), decrypted[-16:]

        HMAC.new(key=mac_key, msg=message).verify(mac_tag=tag)
        return message
    except ValueError:
        print("Get off my lawn or I call the police!!!")
        exit(1)

def main():
    try:
        encrypted_password = base64.b64decode(input('Encrypted password>'))
        password = decrypt(encrypted_password)
        
        if password == PASSWORD:
            print(str(base64.b64encode(encrypt(FLAG)), 'utf-8'))
        else:
            print("Wrong Password!!!")
    except:
        exit(1)

if __name__ == '__main__':
    main()