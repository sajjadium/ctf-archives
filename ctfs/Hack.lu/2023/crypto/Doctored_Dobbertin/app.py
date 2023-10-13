#!/usr/bin/env python3

import secrets
import os, sys

from oracle import TAES_Oracle

FLAG = os.getenv('FLAG')
FLAG = FLAG if "flag" in FLAG else "flag{fake_flag}"
FLAG += " " * (16 - len(FLAG))
assert len(FLAG) == 16

def encrypt_challenge(oracle: TAES_Oracle, challenge: bytes, tweak: str):
    return oracle.encrypt(challenge, tweak)

def main():
    instance = TAES_Oracle()
    init_tweak = secrets.token_hex(16)
    challenge = encrypt_challenge(instance, FLAG.encode(), init_tweak)
    print('Welcome to Doctored Dobbertin!')
    print('''
  _____             _                     _   _____        _     _               _   _       
 |  __ \           | |                   | | |  __ \      | |   | |             | | (_)      
 | |  | | ___   ___| |_ ___  _ __ ___  __| | | |  | | ___ | |__ | |__   ___ _ __| |_ _ _ __  
 | |  | |/ _ \ / __| __/ _ \| '__/ _ \/ _` | | |  | |/ _ \| '_ \| '_ \ / _ \ '__| __| | '_ \ 
 | |__| | (_) | (__| || (_) | | |  __/ (_| | | |__| | (_) | |_) | |_) |  __/ |  | |_| | | | |
 |_____/ \___/ \___|\__\___/|_|  \___|\__,_| |_____/ \___/|_.__/|_.__/ \___|_|   \__|_|_| |_|
                                                                                                                                                                                     
''')
    print()
    print(f"You got a challenge: {challenge.hex()}")
    print(f"Tweak used: {init_tweak}")
    print("Now it's your turn to challenge me.")
    for i in range(7):
        inp = input("Enter your challenge: >")
        tweak_choosen = input("Enter your challenge tweak: >")
        try:
            rx = encrypt_challenge(instance,bytes.fromhex(inp), tweak_choosen).hex()
            print(rx)
        except:
            print("Invalid input. Likely not 16B, 16B.")
            continue
    print('Examination complete.')

if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
