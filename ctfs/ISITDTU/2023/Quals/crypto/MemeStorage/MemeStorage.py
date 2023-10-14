#!/usr/bin/env python3
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import re

def check_name(password):
    if re.fullmatch(r"\w*", password, flags=re.ASCII) and \
        re.search(r"\d", password) and \
        re.search(r"[a-z]", password):
        return True
    return False

secret_key = os.urandom(16)

def encrypt_request(meme_name: str):
    pt = pad(meme_name.encode(), 16)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    return cipher.encrypt(pt).hex()

def decrypt_request(meme_id):
    ct = bytes.fromhex(meme_id)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ct), 16).decode()


# My memes!
meme_storage = {}
meme_storage["meme1"] = os.getenv("MEME1", "Haha")
meme_storage["meme2"] = os.getenv("MEME2", "Hihi")
meme_storage["meme3"] = os.getenv("MEME3", "Hoho")
meme_storage["d4rkbruh"] = os.getenv("FLAG", "ISITDTU{dark_dark_bruh_bruh_lmao_test_flag}")


# create secure AES_GCM authenticated user cookie!
def gen_user_cookie(username, nonce=None):
    if nonce == None:
        nonce = os.urandom(12)
    cookie_dict = {}
    cookie_dict["username"] = username
    cookie_dict["admin_access"] = False
    pt = json.dumps(cookie_dict).encode()
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(pt)
    cookie = nonce.hex() + "." + ct.hex() + "." + tag.hex()
    return cookie


def decode_cookie(cookie):
    cookie = cookie.split(".")
    nonce, ct, tag = [bytes.fromhex(x) for x in cookie]
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag).decode()
    cookie_dict = json.loads(pt)
    return cookie_dict

def check_cookie(cookie):
    if cookie == None:
        return {"error": "No cookie set"}
    try:
        cookie_dict = decode_cookie(cookie)
        assert "username" in cookie_dict and "admin_access" in cookie_dict
    except:
        return {"error": "Something went wrong with your cookie"}
    return cookie_dict


def register(args):
    username = args.get('username')
    if username == None:
        return {"error": "attempted to register without username"}

    # user should control it , right?
    nonce = args.get('nonce')
    if nonce is None:
        cookie = gen_user_cookie(username)
    else:
        nonce = bytes.fromhex(nonce)
        assert len(nonce) == 16
        cookie = gen_user_cookie(username, nonce)

    return {"username": username, "cookie": cookie}


def shareMeme(args: dict):
    user_cookie = args.get('cookie')
    cookie_dict = check_cookie(user_cookie)
    if "error" in cookie_dict:
        return cookie_dict

    meme_name = args.get("meme_name")
    if meme_name == None or not isinstance(meme_name, str):
        return {"error": "How can you add a meme if you don't have a name?"}
    if "d4rkbruh" in meme_name or not check_name(meme_name):
        return {"error": "Nice Try, Hacker!"}
    if meme_name in meme_storage:
        return {"error": "Name collision detected"}
    meme = args.get("meme")
    if meme == None:
        return {"error": "How can you add a meme if you don't have it?"}
    meme_storage[meme_name] = str(meme)
    return {"id": encrypt_request(meme_name)}


def viewMeme(args):
    user_cookie = args.get('cookie')
    cookie_dict = check_cookie(user_cookie)
    if "error" in cookie_dict:
        return cookie_dict

    duck_id = args.get('id')
    try:
        meme_name = decrypt_request(duck_id)
    except:
        return {"error": "something went wrong during decryption of your duck id"}

    if meme_name not in meme_storage:
        return {"error": "Lol! I don't remember that we have it.!"}
    access_level = cookie_dict["admin_access"]

    if  meme_name == "d4rkbruh" and not access_level:
        return {"error": "This meme is too d4rk for you"}
    return {"meme": meme_storage.get(meme_name, )}


def menu():
    print("""
1. Register
2. Add Meme
3. View Meme
4. Exit
""")
    return int(input("> "))

actions = [register, shareMeme, viewMeme]
def main():
    try:
        if os.system("python3 PoW.py") != 0:
            raise Exception("PoW failed")
        while True:
            choice = menu()
            if choice < 1 or choice >= 4:
                raise Exception("Exit")
            args = json.loads(input("Args: "))
            resp = json.dumps(actions[choice-1](args))
            print(resp)
    except:
        print("Bye")


if (__name__ == '__main__'):
    main()
