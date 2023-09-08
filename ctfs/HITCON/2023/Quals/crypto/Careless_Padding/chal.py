#!/usr/local/bin/python
import random
import os
from secret import flag
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json

N = 16

# 0 -> 0, 1~N -> 1, (N+1)~(2N) -> 2 ...
def count_blocks(length):
    block_count = (length-1) // N + 1
    return block_count

def find_repeat_tail(message):
    Y = message[-1]
    message_len = len(message)
    for i in range(len(message)-1, -1, -1):
        if message[i] != Y:
            X = message[i]
            message_len = i + 1
            break
    return message_len, X, Y

def my_padding(message):
    message_len = len(message)
    block_count = count_blocks(message_len)
    result_len =  block_count * N
    if message_len % N == 0:
        result_len += N
    X = message[-1]
    Y = message[(block_count-2)*N+(X%N)]
    if X==Y:
        Y = Y^1
    padded = message.ljust(result_len, bytes([Y]))
    return padded

def my_unpad(message):
    message_len, X, Y = find_repeat_tail(message)
    block_count = count_blocks(message_len)
    _Y = message[(block_count-2)*N+(X%N)]
    if (Y != _Y and Y != _Y^1):
        raise ValueError("Incorrect Padding")
    return message[:message_len]

def chal():
    k = os.urandom(16)
    m = json.dumps({'key':flag}).encode()

    iv = os.urandom(16)
    cipher = AES.new(k, AES.MODE_CBC, iv)

    padded = my_padding(m)
    enc = cipher.encrypt(padded)
    print(f"""
*********************************************************
You are put into the careless prison and trying to escape.
Thanksfully, someone forged a key for you, but seems like it's encrypted... 
Fortunately they also leave you a copied (and apparently alive) prison door.
The replica pairs with this encrypted key. Wait, how are this suppose to help?
Anyway, here's your encrypted key: {(iv+enc).hex()}
*********************************************************
""")

    while True:
        enc = input("Try unlock:")
        enc = bytes.fromhex(enc)
        iv = enc[:16]
        cipher = AES.new(k, AES.MODE_CBC, iv)
        try:
            message = my_unpad(cipher.decrypt(enc[16:]))
            if message == m:
                print("Hey you unlock me! At least you know how to use the key")
            else:
                print("Bad key... do you even try?")
        except ValueError:
            print("Don't put that weirdo in me!")
        except Exception:
            print("What? Are you trying to unlock me with a lock pick?")

if __name__ == "__main__":
    chal()
