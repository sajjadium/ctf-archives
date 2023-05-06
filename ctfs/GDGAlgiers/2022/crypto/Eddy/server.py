#!/usr/bin/python3

import sys
from  challenge import *
from Crypto.Util.number import *


with open("flag.txt","r") as f:
    flag = f.read()

flag = flag.encode()
sk = create_signing_key()
pk = create_verifying_key(sk)
R_flag,S_flag,e_flag = signature(flag,sk,pk)

def start():
    print("Welcom to my singing server !")
    print("-" * 10 + "Menu" + "-" * 10)
    print("1- Sign a message with a random private key ")
    print("2- Sign a message with your private key ")
    print("3- Verify the flag")
    print("4- Quit")
    print("-" * 24)

    try:
        while True:
            c = input("> ")

            if c == '1':
                msg =input("Enter your message : ").encode()
                pk = create_verifying_key(sk)
                R,S,e = signature(msg,sk,pk)
                out = {"R":R,"S": S,"e":e}
                print(out)
            elif c == '2':
                msg = input("Enter your message : ").encode()
                privk = int(input("Enter your private key : "))
                privk = long_to_bytes(privk)
                pk =  create_verifying_key(privk)
                R, S, e = signature(msg, sk, pk)
                out = {"R": R, "S": S, "e": e}
                print(out)
            elif c == '3':
                pk = int(input("Enter your public key  : "))
                pk = long_to_bytes(pk)
                if checkvalid(R_flag+scalar_to_bytes(S_flag),flag,pk):
                    print("You are an admin, Here's your flag ", flag)
                else:
                    print("Sorry , you can't get your flag !")
                    sys.exit()


            elif c == '4':
                print("Goodbye :)")
                sys.exit()

    except Exception:
        print("System error.")
        sys.exit()

start()