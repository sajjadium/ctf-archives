#!/usr/local/bin/python3.10 -u

import time
from Crypto.Util.number import getPrime, getRandomInteger, getRandomNBitInteger

flag = open("flag.txt").read().strip()
p = getPrime(512)
q = getPrime(512)

sub = getRandomInteger(20)

# hehe u cant guess it since its random :P
my_password = getRandomNBitInteger(256)

n = p*q
c = pow(my_password, 65537, n)
dont_leak_this = (p-sub)*(q-sub)


def gamechat():
    print("<Bobby> i have an uncrackable password maybe")
    print(f"<Bobby> i'll give you the powerful numbers, {c} and {n}")
    print("<Bobby> gl hacking into my account")
    print("<Bobby> btw do you want to get my diamond stash")
    resp = input("<You> ")
    if (resp.strip() == "yea"):
        print("<Bobby> i'll send coords")
        print(f"<Bobby> {dont_leak_this}")
        print("<Bobby> oop wasnt supposed to copypaste that")
        print("<Bobby> you cant crack my account tho >:)")
        tic = time.time()
        resp = input("<You> ")
        toc = time.time()
        if (toc-tic >= 2.5):
            print("<Bobby> you know I can reset my password faster than that lol")
        elif (resp.strip() != str(my_password)):
            print("<Bobby> lol nice try won't give password that easily")
        else:
            print("<Bobby> NANI?? Impossible?!?")
            print("<Bobby> I might as wel give you the flag")
            print(f"<Bobby> {flag}")
    else:
        print("<Bobby> bro what, who denies free diamonds?")
    print("Bobby has left the game")


gamechat()
