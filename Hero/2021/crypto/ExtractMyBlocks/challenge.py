#!/usr/bin/env python3
from os import getenv
from Crypto.Cipher import AES

BLOCK_SIZE = 16
FLAG = getenv("FLAG")
KEY = getenv("KEY")


padding = lambda msg: msg + "0" * (BLOCK_SIZE - len(msg) % BLOCK_SIZE)
encrypt = lambda plain: AES.new(KEY, AES.MODE_ECB).encrypt(plain).hex()

print("[SUPPORT] Password Reset")
account_id = input("Please enter your account ID : ")

msg = f"""
Welcome back {account_id} !

Your password : {FLAG}

Regards
"""
print(encrypt(padding(msg)))
