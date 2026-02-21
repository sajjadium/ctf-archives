from Crypto.Cipher import DES3, DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def adjust_key(key8: bytes) -> bytes:
    out = bytearray()
    for b in key8:
        b7 = b & 0xFE                
        ones = bin(b7).count("1")     
        out.append(b7 | (ones % 2 == 0))  
    return bytes(out)

flag = b'REDACTED'
k1 = adjust_key(get_random_bytes(8))

def triple_des(pt, k2, k3):
    cipher = DES3.new(k3 + k2 + k1, DES3.MODE_ECB)
    return cipher.encrypt(pad(pt, 8))

def triple_des_ultra_secure_v1(pt, k2, k3):
    cipher1 = DES.new(k1, DES.MODE_ECB)
    cipher2 = DES.new(k2, DES.MODE_ECB)
    cipher3 = DES.new(k3, DES.MODE_ECB)

    return cipher1.encrypt(cipher2.encrypt(cipher3.encrypt(pad(pt, 8))))

def triple_des_ultra_secure_v2(pt, k2, k3):
    cipher1 = DES.new(k1, DES.MODE_ECB)
    cipher2 = DES.new(k2, DES.MODE_ECB)
    cipher3 = DES.new(k3, DES.MODE_ECB)

    return cipher1.decrypt(cipher2.encrypt(cipher3.encrypt(pad(pt, 8))))

while True:
    print("I will prove its secure af by letting you choose k2 and k3")
    k2 = adjust_key(bytes.fromhex(input("enter k2 hex bytes >")))
    k3 = adjust_key(bytes.fromhex(input("enter k3 hex bytes >")))
    
    print("1. triple des\n2. ultra secure v1\n3. ultra secure v2\n4. exit")
    option = int(input("enter option >"))

    print("1. encrypt flag\n2. encrypt your own text")
    option_ = int(input("enter option >"))
    
    if k2 == k3:
        print("ok its not thaaat secure, try again")
        continue

    if option_ == 2:
        pt = bytes.fromhex(input("enter hex bytes >"))
    else:
        pt = flag
    if option == 1:
        print(f"ciphertext : {triple_des(pt, k2, k3).hex()}")
    elif option == 2:
        print(f"ciphertext : {triple_des_ultra_secure_v1(pt, k2, k3).hex()}")
    elif option == 3:
        print(f"ciphertext : {triple_des_ultra_secure_v2(pt, k2, k3).hex()}")
    else:
        exit()