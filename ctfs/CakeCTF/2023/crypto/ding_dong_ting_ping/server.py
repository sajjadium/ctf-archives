import os
from base64 import b64decode, b64encode
from hashlib import md5
from datetime import datetime
from Crypto.Cipher import AES

FLAG = os.environ.get("FLAG", "neko{cat_does_not_eat_cake}")
PREFIX = os.environ.get("PREFIX", "cake").encode()

KEY = os.urandom(16)
IV = os.urandom(16)
aes = AES.new(KEY, AES.MODE_ECB)

xor = lambda a, b: bytes([x^y for x, y in zip(a, b)])

def pad(data: bytes):
    l = 16 - len(data) % 16
    return data + bytes([l]*l)

def unpad(data: bytes):
    return data[:-data[-1]]

def encrypt(plain: bytes):
    plain = pad(plain)
    blocks = [plain[i:i+16] for i in range(0, len(plain), 16)]
    ciphers = [IV]
    for block in blocks:
        block = xor(block, md5(ciphers[-1]).digest())
        ciphers.append(aes.encrypt(block))
    return b"".join(ciphers)

def decrypt(cipher: bytes):
    blocks = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
    h = md5(blocks[0]).digest() # IV
    plains = []
    for block in blocks[1:]:
        plains.append(xor(aes.decrypt(block), h))
        h = md5(block).digest()
    return unpad(b"".join(plains))    

def register():
    username = b64decode(input("username(base64): ").strip())
    if b"root" in username:
        print("Cannot register as root user!")
    else:
        cookie = b"|".join([PREFIX, b"user="+username, str(datetime.now()).encode()])
        cookie = encrypt(cookie)
        cookie = b64encode(cookie)
        print("your cookie =>", cookie.decode())
    return

def login():
    cookie = input("cookie: ").strip()
    cookie = decrypt(b64decode(cookie))
    data = cookie.split(b"|")
    if (data[0] == PREFIX) and data[1].startswith(b"user="):
        username = data[1].split(b"=")[1]
        time = data[2]
    else:
        print("Authentication unsuccessful...")
        return
    print(f"Hi, {username.decode()}! [registered at {time.decode()}]")
    if username != b"root":
        print("You're not the root user...")
    else:
        print("Ding-Dong, Ding-Dong, Welcome, root. The ultimate authority has logged in.")
        print("This is for you => ", FLAG)
    return

while True:
    print("===== MENU =====")
    choice = int(input("[1]register [2]login: ").strip())
    if choice == 1:
        register()
    elif choice == 2:
        login()
    else:
        print("Invalid choice")
    print()
