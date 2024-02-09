from Crypto.Util.number import * 
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import os
import random
import json
key = os.urandom(16)
Flag = '0xL4ugh{Fak3_Fl@g}'
max_retries=19
def evilRSA(seed):
    d = 1 
    while d.bit_length() != int(seed[6:9]): 
        d = getPrime(int(seed[6:9]))
        while not isPrime(d>>333):
            d = getPrime(int(seed[6:9]))
    return d 

def RsaGen(d):
    for _ in range(max_retries):
        try:
            Ns, es = [], []
            for evilChar in '666':
                p = getPrime(512)
                q = getPrime(512)
                phi = (p - 1) * (q - 1)
                e = inverse(d, phi)
                Ns.append(p * q)
                es.append(e)
            
            return Ns, es
        except ValueError as e:
            # Ignore the error and continue the loop
            pass

def getrand(good):
    user_input = int(input("Enter your payload:\t"))
    if user_input.bit_length() > (666//2): 
        print("MEH")
        return 
    return [good*user_input + getPrime(666//2) for i in range(10)]

def encrypt(pt):
    IV = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(pt.encode(), 16))
    return IV.hex() + encrypted.hex()

def decrypt(ct):
    try:
        IV = bytes.fromhex(ct[:32])
        cipher = AES.new(key, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(bytes.fromhex(ct[32:]))
    except ValueError as decryption_error:
        print("AES Decryption Error:", decryption_error)
        return None

    try:
        plaintext = unpad(decrypted, 16).decode()
    except ValueError as unpadding_error:
        print("Unpadding Error:", decrypted)
        return None

    return plaintext

def flag(data):
    data=json.loads(data)
    print('1. Get Flag')
    print('2.Exit')
    while True:
        print('1. Get Flag')
        print('2.Exit')
        z = json.loads(input())
        if z['option'] == '1':
            if isinstance(data, dict) and data['isadmin'] == True:
                print(Flag)
            else:
                print('Try another time')
        elif z['option'] == '2':
            return