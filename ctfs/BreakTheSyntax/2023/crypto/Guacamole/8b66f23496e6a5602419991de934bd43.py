from guacamole import *
from hashlib import md5
from os import urandom


with open('flag', 'r') as f:
    flag = f.read()

destinations = []
key = urandom(16)
iv_len = 96
flag_iv = urandom(96//8)
flag_ct, flag_t = aes_gua_encrypt(pt=flag.encode(), key=key, iv=flag_iv, additional_data=b"flag", t=136)

def connect(destination: bytes):
    if destination in destinations:
        print("CONNECTION REQUEST FAILED: ALREADY CONNECTED")
        return

    destinations.append(destination)

    for i in range(5):    
        # I've read in the standard that IV should
        # be generated deterministically, don't know
        # why tho
        iv = md5(destination + i.to_bytes(2, 'big')).digest()[:iv_len//8]
        ct, flag_t = aes_gua_encrypt(pt=urandom(4), key=key, iv=iv, additional_data=b"handshake", t=136)
        print("ct =", ct.hex())
        print("iv =", iv.hex())
        print("t =", flag_t.hex())        

def parse_message(ct: bytes, t: bytes, A: bytes, iv: bytes):
    try:
        pt = aes_gua_decrypt(ct=ct, key=key, iv=iv, additional_data=A, t=136, tag=t)
    except Exception as E:
        print("Decryption error")
        return
    try:
        pt = pt.decode("ascii")
    except:
        print("Parsing error")
        return
    if pt == flag and flag_t != t and A == b"You're mine.":
        print("flag =", flag)

if __name__ == "__main__":
    print("We've intercepted this important message. Forge a new signature for it!")
    print("flag ct =", flag_ct.hex())
    print("flag iv =", flag_iv.hex())
    print("flag t =", flag_t.hex())  

    while True:
        print("You're in their walls. What do you want to do?")
        print("[1] Send connection request", "[2] Forge message", "[3] exit",sep="\n")
        sel = int(input(">"))
        if sel == 1:
            dest = bytes.fromhex(input("Destination:\n(hex)>"))
            connect(dest)
        if sel == 2:
            ct = bytes.fromhex(input("ct:\n(hex)>"))
            add = bytes.fromhex(input("add. data:\n(hex)>"))
            iv = bytes.fromhex(input("iv:\n(hex)>"))
            t = bytes.fromhex(input("tag:\n(hex)>"))
            parse_message(ct=ct, t=t, A=add, iv=iv)
        if sel == 3: 
            exit(0)



