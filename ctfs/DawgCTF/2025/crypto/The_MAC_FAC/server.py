#!/usr/local/bin/python3
from Crypto.Cipher import AES
from Crypto.Util.strxor import *
from Crypto.Util.number import *
from Crypto.Util.Padding import *
from secret import flag, xor_key, mac_key, admin_iv, admin_phrase
import os

banner  = """
Welcome to the MAC FAC(tory). Here you can request prototype my secure MAC generation algorithm. I know no one can break it so I hid my flag inside the admin panel, but only I can access it. Have fun! 
"""
menu1 = """
[1] - Generate a MAC 
[2] - Verify a MAC
[3] - View MAC Logs
[4] - View Admin Panel
[5] - Exit
"""
admin_banner = """
There's no way you got in! You have to be cheating this bug will be reported and I will return stronger!
""" + flag

def xor(data: bytes, key: bytes) -> bytes: #Installing pwntools in docker was giving me issues so I have to port over xor from strxor
    repeated_key = (key * (len(data) // len(key) + 1))[:len(data)]
    return strxor(data, repeated_key)

assert(len(mac_key) == 16)
assert(len(xor_key) == 16)

logs = []

def CBC_MAC(msg, iv):
    cipher = AES.new(mac_key, AES.MODE_CBC, iv) # Encrypt with CBC mode
    padded = pad(msg, 16) # Pad the message
    tag = cipher.encrypt(padded)[-16:] # only return the last block as the tag
    msg_enc, iv_enc = encrypt_logs(padded, iv)
    logs.append((f"User generated a MAC (msg={msg_enc.hex()}, IV={iv_enc.hex()}"))
    return tag

def encrypt_logs(msg, iv):
    return (xor(msg, xor_key), xor(iv, xor_key))#Encrypts logs so users can't see other people's IVs and Messages
    
def verify(msg, iv, tag):
    cipher = AES.new(mac_key, AES.MODE_CBC, iv)
    padded = pad(msg, 16)
    candidate = cipher.encrypt(padded)[-16:]
    return candidate == tag

def view_logs():
    print("\n".join(logs))
    return

def setup_admin():
    tag = CBC_MAC(admin_phrase, admin_iv)
    return tag

def verify_admin(msg, iv, user_tag, admin_tag):
    if msg == admin_phrase:
        print("This admin phrase can only be used once!")
        return
    
    tag = CBC_MAC(msg, iv)
    if (tag != user_tag): #Ensure msg and iv yield the provided tag
        print("Computed: ", tag.hex())
        print("Provided: ", user_tag.hex())
        print("Computed MAC Tag doesn't match provided tag")
        return
    else:
        if (tag == admin_tag):
            print(admin_banner)
            return
        else:
            print("Tag is invalid")

def run():
    admin_tag = setup_admin()
    print(banner)
    while True:
        print(menu1)
        usr_input = input("> ")
        if usr_input == "1":
            msg = input("Message: ")
            print(msg)
            if (len(msg.strip()) == 0):
                print("Please input a valid message")
                continue
            iv = bytes.fromhex(input("IV (in hex): ").strip())
            if (len(iv) != 16):
                print("The IV has to be exactly 16 bytes")
                continue
            tag = CBC_MAC(msg.encode(), iv)
            print("The MAC Tag for your message is: ", tag.hex())
            continue
        if usr_input == "2":
            msg = input("Message: ")
            if (len(msg.strip()) == 0):
                print("Please input a valid message")
                continue
            iv = bytes.fromhex(input("IV (in hex): ").strip())
            if (len(iv) != 16):
                print("The IV has to be exactly 16 bytes")
                continue
            tag = bytes.fromhex(input("Tag (in hex): ").strip())
            if (len(tag) != 16):
                print("The MAC has to be exactly 16 bytes")
                continue
            valid = verify(msg.encode(), iv, tag)
            if valid:
                print("The tag was valid!")
            else:
                print("The tag was invalid!")
            continue
        if usr_input == "3":
            view_logs()
            continue
        if usr_input == "4":
            msg = input("Admin passphrase: ")
            if (len(msg.strip()) == 0):
                print("Please input a valid message")
                continue
            iv = bytes.fromhex(input("IV (in hex): ").strip())
            if (len(iv) != 16):
                print("The IV has to be exactly 16 bytes")
                continue
            tag = bytes.fromhex(input("Tag (in hex): ").strip())
            if (len(tag) != 16):
                print("The MAC has to be exactly 16 bytes")
                continue
            verify_admin(msg.encode(), iv, tag, admin_tag)
            continue
        if usr_input == "5":
            break
    exit()
            

if __name__ == '__main__':
    run()
