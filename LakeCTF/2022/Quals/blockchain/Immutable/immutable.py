#!/usr/bin/env -S python3 -u

LOCAL = False # Set this to true if you want to test with a local hardhat node, for instance

#############################

import os.path, hashlib, hmac
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASE_PATH, "key")) as f:
    KEY = bytes.fromhex(f.read().strip())

if LOCAL:
    from web3.auto import w3 as web3
else:
    from web3 import Web3, HTTPProvider
    web3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"))

def gib_flag():
    with open(os.path.join(BASE_PATH, "flag.txt")) as f:
        print(f.read().strip())

def auth(addr):
    H = hmac.new(KEY, f"{int(addr, 16):40x}".encode(), hashlib.blake2b)
    return H.hexdigest()

def audit():
    addr = input("Where is your contract? ")
    code = web3.eth.get_code(addr)
    if not code:
        print("Haha, very funny, a contract without code...")
        return
    if target(addr) in code:
        print("Oh, you criminal!")
    else:
        print("Alright then, here's some proof that that contract is trustworthy")
        print(auth(addr))

def target(addr):
    return hashlib.sha256(f"{int(addr, 16):40x}||I will steal all your flags!".encode()).digest()

def rugpull():
    addr = input("Where is your contract? ")
    proof = input("Prove you're not a criminal please.\n> ")
    if auth(addr) != proof:
        print("I don't trust you, I won't invest in your monkeys")
        return
    print("Oh, that looks like a cool and safe project!")
    print("I'll invest all my monopoly money into this!")
    code = web3.eth.get_code(addr)
    if target(addr) in code:
        gib_flag()
    else:
        print("Oh, I guess my money actually *is* safe, somewhat...")

if __name__ == "__main__":
    choice = input("""What do you want to do?
1. Perform an audit
2. Pull the rug
3. Exit
> """).strip()
    {"1": audit, "2": rugpull}.get(choice, exit)()
