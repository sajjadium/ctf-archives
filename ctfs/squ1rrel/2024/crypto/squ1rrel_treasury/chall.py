from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.strxor import strxor
from Crypto.Cipher import AES
import os
from secrets import KEY, FLAG
import random

ACCOUNT_NAME_CHARS = set([chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)])
FLAG_COST = random.randint(10**13, 10**14-1)

def blockify(text: str, block_size: int):
    return [text[i:i+block_size] for i in range(0, len(text), block_size)]

def pad(blocks: list, pad_char: chr, size: int):
    padded = []
    for block in blocks:
        tmp = block
        if len(block) < size:
            tmp = tmp + pad_char*(size-len(tmp))
        elif len(block) > size:
            print("Inconsistent block size in pad")
            exit(1)
        padded.append(tmp)
    return padded

class Account:
    def __init__(self, iv: bytes, name: str, balance: int):
        self.__iv = iv
        self.__name = name
        self.__balance = balance

    def getIV(self):
        return self.__iv

    def getName(self):
        return self.__name

    def getBalance(self):
        return self.__balance

    def setBalance(self, new_balance):
        self.__balance = new_balance

    def getKey(self):
        save = f"{self.__name}:{self.__balance}".encode()
        blocks = blockify(save, AES.block_size)
        pblocks = pad(blocks, b'\x00', AES.block_size)
        cipher = AES.new(KEY, AES.MODE_ECB)
        ct = []
        for i, b in enumerate(pblocks):
            if i == 0:
                tmp = strxor(b, self.__iv)
                ct.append(cipher.encrypt(tmp))
            else:
                tmp = strxor(strxor(ct[i-1], pblocks[i-1]), b)
                ct.append(cipher.encrypt(tmp))
        ct_str = f"{self.__iv.hex()}:{(b''.join(ct)).hex()}"
        return ct_str

    def load(key: str):
        key_split = key.split(':')
        iv = bytes.fromhex(key_split[0])
        ct = bytes.fromhex(key_split[1])
        cipher = AES.new(KEY, AES.MODE_ECB)
        pt = blockify(cipher.decrypt(ct), AES.block_size)
        ct = blockify(ct, AES.block_size)
        for i, p in enumerate(pt):
            if i == 0:
                pt[i] = strxor(p, iv)
            else:
                pt[i] = strxor(strxor(ct[i-1], pt[i-1]), p)
        pt = b''.join(pt)
        pt_split = pt.split(b':')
        try:
            name = pt_split[0].decode()
        except Exception:
            name = "ERROR"
        balance = int(pt_split[1].strip(b'\x00').decode())
        return Account(iv, name, balance)

def accountLogin():
    print("\nPlease provide your account details.")
    account = input("> ").strip()
    account = Account.load(account)
    print(f"\nWelcome {account.getName()}!")
    while True:
        print("What would you like to do?")
        print("0 -> View balance")
        print(f"1 -> Buy flag ({FLAG_COST} acorns)")
        print("2 -> Save")
        opt = int(input("> ").strip())
        if opt == 0:
            print(f"Balance: {account.getBalance()} acorns\n")
        elif opt == 1:
            if account.getBalance() < FLAG_COST:
                print("Insufficient balance.\n")
            else:
                print(f"Flag: {FLAG}\n")
                account.setBalance(account.getBalance()-FLAG_COST)
        elif opt == 2:
            print(f"Save key: {account.getKey()}\n")
            break                


def accountNew():
    print("\nWhat would you like the account to be named?")
    account_name = input("> ").strip()
    dif = set(account_name).difference(ACCOUNT_NAME_CHARS)
    if len(dif) != 0:
        print(f"Invalid character(s) {dif} in name, only letters allowed!")
        print("Returning to main menu...\n")
        return
    account_iv = os.urandom(16)
    account = Account(account_iv, account_name, 0)
    print(f"Wecome to Squirrel Treasury {account.getName()}")
    print(f"Here is your account key: {account.getKey()}\n")

if __name__ == "__main__":
    while True:
        print(r"""
              ⠀⠀⠀⠀⠀⠀⠀ ⢀⣀⣤⣄⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⢴⣶⠀⢶⣦⠀⢄⣀⠀⠠⢾⣿⠿⠿⠿⠿⢦⠀⠀ ___  __ _ _   _/ |_ __ _ __ ___| |           
⠀⠀⠀⠀⠀⠀⠀⠀⠺⠿⠇⢸⣿⣇⠘⣿⣆⠘⣿⡆⠠⣄⡀⠀⠀⠀⠀⠀⠀⠀/ __|/ _` | | | | | '__| '__/ _ \ |            
⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⣤⣄⡉⠛⠀⢹⣿⡄⢹⣿⡀⢻⣧⠀⡀⠀⠀⠀⠀⠀\__ \ (_| | |_| | | |  | | |  __/ |            
⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡈⠓⠀⣿⣧⠈⢿⡆⠸⡄⠀⠀⠀⠀|___/\__, |\__,_|_|_|  |_|  \___|_|            
⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣈⠙⢆⠘⣿⡀⢻⠀⠀⠀⠀        |_|                                    
⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠹⣧⠈⠀⠀⠀⠀ _____                                         
⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠈⠃⠀⠀⠀⠀/__   \_ __ ___  __ _ ___ _   _ _ __ ___ _   _ 
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀  / /\/ '__/ _ \/ _` / __| | | | '__/ _ \ | | |
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀ / /  | | |  __/ (_| \__ \ |_| | | |  __/ |_| |
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀ \/   |_|  \___|\__,_|___/\__,_|_|  \___|\__, |
⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀                                         |___/ 
⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⣿⠿⠿⠿⠿⠿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
              """)
        print("Welcome to squ1rrel Treasury! What would you like to do?")
        print("0 -> Login")
        print("1 -> Create new account")
        opt = int(input("> ").strip())
        if opt == 0:
            accountLogin()
        elif opt == 1:
            accountNew()
