#!/usr/bin/env -S python3 -u

LOCAL = False # Set this to true if you want to test with a local hardhat node, for instance

#############################

import os.path, hashlib, hmac
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

if LOCAL:
    from web3.auto import w3 as web3
else:
    from web3 import Web3, HTTPProvider
    web3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"))

web3.codec._registry.register_decoder("raw", lambda x: x.read(), label="raw")

def gib_flag():
    with open(os.path.join(BASE_PATH, "flag.txt")) as f:
        print(f.read().strip())

def verify(addr):
    code = web3.eth.get_code(addr)
    if not 0 < len(code) < 8:
        return False

    contract = web3.eth.contract(addr, abi=[ { "inputs": [], "name": "quinevm", "outputs": [ { "internalType": "raw", "name": "", "type": "raw" } ], "stateMutability": "view", "type": "function" } ])
    return contract.caller.quinevm() == code

if __name__ == "__main__":
    addr = input("addr? ").strip()
    if verify(addr):
        gib_flag()
    else:
        print("https://i.imgflip.com/34mvav.jpg")
