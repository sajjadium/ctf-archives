#!/usr/bin/env python3
from topsecrets import iv, key, secret_msg, secret_tag, FLAG
from Crypto.Cipher import AES

iv = bytes.fromhex(iv)

menu = """
/===== MENU =====\\
|                |
|  [M] MAC Gen   |
|  [A] AUTH      |
|                |
\================/
"""

def MAC(data):    
    assert len(data) % 16 == 0, "Invalid Input"
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
    print(secret_msg)
    try:
        for _ in range(3):
            print(menu)
            ch = input("[?] Choice: ").strip().upper()
            if ch == 'M':
                data = input("[+] Enter plaintext(hex): ").strip()
                tag = MAC(bytes.fromhex(data))
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