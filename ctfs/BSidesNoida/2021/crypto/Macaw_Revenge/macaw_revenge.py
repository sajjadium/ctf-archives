#!/usr/bin/env python3
from Crypto.Cipher import AES
import os

with open('flag.txt') as f:
    FLAG = f.read()


menu = """
/===== MENU =====\\
|                |
|  [M] MAC Gen   |
|  [A] AUTH      |
|                |
\================/
"""

def MAC(data, check=False):    
    assert len(data) % 16 == 0, "Invalid Input"
    
    if check:
        assert data != secret_msg, "Not Allowed!!!"
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    tag = cipher.encrypt(data)[-16:]
    return tag.hex()

def AUTH(tag):
    if tag == secret_tag:
        print("[-] Successfully Verified!\n[-] Details:", FLAG)
    else:
        print("[-] Verification Flaied !!!")

if __name__ == "__main__":
    iv = os.urandom(16)
    key = os.urandom(16)
    secret_msg = os.urandom(48)
    secret_tag = MAC(secret_msg)

    print(f"[+] Forbidden msg: {secret_msg.hex()}")
    try:
        for _ in range(3):
            print(menu)
            ch = input("[?] Choice: ").strip().upper()
            if ch == 'M':
                data = input("[+] Enter plaintext(hex): ").strip()
                tag = MAC(bytes.fromhex(data), check=True)
                print("[-] Generated tag:", tag)
                print("[-] iv:", iv.hex())
            elif ch == 'A':
                tag = input("[+] Enter your tag to verify: ").strip()
                AUTH(tag)
            else:
                print("[!] Invalid Choice")
                exit()
    except Exception as e:
        print(":( Oops!", e)
        print("Terminating Session!")