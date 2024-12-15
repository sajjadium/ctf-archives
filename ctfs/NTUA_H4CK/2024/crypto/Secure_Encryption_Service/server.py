from Crypto.Cipher import AES
from time import time
from hashlib import sha256
from secret import FLAG

key = sha256(sha256(str(int(time())).encode() + FLAG).digest() + FLAG).digest()

cipher = AES.new(key= key, mode= AES.MODE_CTR, nonce= sha256(FLAG + sha256(FLAG + str(int(time())).encode()).digest()).digest()[:12])

MENU = '''Options:
1. Encrypt flag
2. Encrypt your own plaintext'''

while True:
    print(MENU)
    option = input("> ")
    try:
        option = int(option)
    except ValueError:
        break

    if option == 1:
        print(cipher.encrypt(FLAG).hex())
    elif option == 2:
        pt = input("your plaintext: ")
        try:
            pt = bytes.fromhex(pt)
        except ValueError:
            break
        print(cipher.encrypt(pt).hex())
    else:
        print(sha256(b'Nice try, now give me a valid option').hexdigest())

