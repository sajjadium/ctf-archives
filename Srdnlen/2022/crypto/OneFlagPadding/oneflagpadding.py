#!/usr/bin/env python3

import random
import string
from Crypto.Util.number import getPrime, bytes_to_long


def flag_padding(flag):
    s = string.ascii_lowercase + string.ascii_uppercase + string.digits
    for i in range(random.randint(5, 10)):
        flag = random.choice(s) + flag + random.choice(s)
    return flag


def message_padding(message, flag):
    return message + flag


flag = open("flag.txt", "r").read()
flag = flag_padding(flag)
p = getPrime(512)
q = getPrime(512)
n = p*q
e = 7

encrypted_flag = pow(bytes_to_long(flag.encode()), e, n)
print("This is the flag: ", encrypted_flag)
print("Give any message you want, I will pad it with my special flag and encrypt it")
msg = input("> ")
if len(msg) < 10:
    print("Message to small, you are not gonna trick me")
    exit()
final_msg = message_padding(msg, flag)
ct = pow(bytes_to_long(final_msg.encode()), e, n)

print("Here is your ciphertext")
print("e: ", e)
print("n: ", n)
print("enc_message: ", ct)
