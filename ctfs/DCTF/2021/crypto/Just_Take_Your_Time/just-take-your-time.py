#!/usr/bin python3

from flag import flag
from Crypto.Cipher import DES3
from time import time
from random import randint
from secrets import token_hex
from pytimedinput import timedInput

guess = 3
TIMEOUT = 1

a = randint(1000000000000000, 9999999999999999)
b = randint(1000000000000000, 9999999999999999)

print("Show me you are worthy and solve for x! You have one second.")
print("{} * {} = ".format(a, b))

answ, _ = timedInput("> ", timeOut = 1, forcedTimeout = True)

try:
    assert(a*b == int(answ))
except:
    print("You are not worthy!")
    exit(1)

key = str(int(time())).zfill(16).encode("utf-8")
secret = token_hex(16)
cipher = DES3.new(key, DES3.MODE_CFB, b"00000000")
encrypted = cipher.encrypt(secret.encode("utf-8"))
print("You have proven yourself to be capable of taking on the final task. Decrypt this and the flag shall be yours!")
print(encrypted.hex())

start_time = time()
while(time() - start_time < TIMEOUT and guess > 0):
    delta = time() - start_time
    answ, _ = timedInput("> ", timeOut = TIMEOUT + 1 - delta, forcedTimeout = True)

    try:
        assert(secret == answ)
        break
    except:
        if answ != "":
            guess -= 1
            if (guess != 1):
                print("You are wrong. {} guesses remain.".format(guess))
            else:
                print("You are wrong. {} guess remains.".format(guess))

if (secret != answ):
    print("You have been unsuccessful in your quest for the flag.")
else:
    print("Congratulations! Here is your flag.")
    print(flag)
