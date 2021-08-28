#!/usr/bin/env python3.8
from Crypto.Util.number import getStrongPrime, inverse
from json import loads, dumps
import hashlib, sys, os, signal, random

FLAG = "FwordCTF{###############################}"

WELCOME = '''
                 ______________
               _(______________()
  ______     _- |              ||
 |      |_ _-   |              ||
 |      |_|_    |  Boombastic  ||
 |______|   -_  |              ||
    /\\        -_|______________||
   /  \\        
  /    \\       
 /      \\     
'''

p = getStrongPrime(1024)
secret = random.randint(1, p-1)

def get_ticket(code):
    y = int(hashlib.sha256(code.encode()).hexdigest(),16)
    r = ((y**2 - 1) * (inverse(secret**2, p))) % p
    s = ((1 + y) * (inverse(secret, p))) % p
    return {'s': hex(s), 'r': hex(r), 'p': hex(p)}


class Boombastic:
    def __init__(self):
        print(WELCOME)

    def start(self):
        try:
            while True:
                print("\n1- Enter Cinema")
                print("2- Get a ticket")
                print("3- Leave")
                c = input("> ")

                if c == '1':
                    magic_word = loads(input("\nEnter the magic word : "))
                    if magic_word == get_ticket("Boombastic"):
                        print(f"Here is your flag : {FLAG}, enjoy the movie sir.")
                    else:
                        print("Sorry, VIPs only.")
                        sys.exit()

                elif c == '2':
                    word = os.urandom(16).hex()
                    print(f"\nYour ticket : {dumps(get_ticket(word))}")

                elif c == '3':
                    print("Goodbye :)")
                    sys.exit()

        except Exception:
            print("System error.")
            sys.exit()
        
        
signal.alarm(360)
if __name__ == "__main__":
    challenge = Boombastic()
    challenge.start()