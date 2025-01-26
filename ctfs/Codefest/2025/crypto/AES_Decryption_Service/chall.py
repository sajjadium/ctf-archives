import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = ?
KEY = ?

def encryptflag():
    cipher = AES.new(KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    return ciphertext.hex()

def decrypt(ciphertext, iv):
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.hex()

print("AES Decryption Service\n")
print(f"Encrypted Flag: {encryptflag()}\n")

while True: 
    try:
        IN = input('>>> ')
        IN = bytes.fromhex(IN)
        IV, CT = IN[:16], IN[16:]
        print(decrypt(CT, IV) + '\n')
    except ValueError:
        print('Invalid Input\n')
        continue
    except:
        print('\nOK Bye')
        break