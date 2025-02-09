#!/usr/local/bin/python3
import os
import sys
from tiny import Cipher
from dotenv import load_dotenv
from Crypto.Util.number import long_to_bytes as l2b

load_dotenv()
FLAG = os.getenv("FLAG")
WELCOME_MSG = (r""" 
****************************************************************
___________.__              _________ .__           .__        
\__    ___/|__| ____ ___.__.\_   ___ \|  |__ _____  |__| ____  
  |    |   |  |/    <   |  |/    \  \/|  |  \\__  \ |  |/    \ 
  |    |   |  |   |  \___  |\     \___|   Y  \/ __ \|  |   |  \
  |____|   |__|___|  / ____| \______  /___|  (____  /__|___|  /
                   \/\/             \/     \/     \/        \/ 

****************************************************************          
""")

BLOCKS = [
    "c8fdee0e9a5b943cf3c9349074b3daa1e6edc40c4420194878914fa06d3ac668",
    "fb7d8c559e45cc6afb386e67709712ca44bd0245474b10ad7f5e71ba086e2e3e",
    "5b92f3c0d8ab00008455805f02cbeb6ba492f6adeb294ab06cd916ac9062301d",
    "9e962d3c42acde05ac7969759294cd66fe52ed63da9e4614a07a27b5522bb919",
    "e32bedda93141e19cf30e96f38323fc78e719da0b6d7fd5017cc7b5c3725a674",
    "86d3af23ae717180000f57e55865e9e4dfeed2e629ae1c80b91f0785da6d5f61",
]

def encrypt_with_tea(msg, key):
    cipher = Cipher(key)
    if isinstance(msg, str):
        msg = msg.encode()
    return cipher.encrypt(msg)

def validate_blocks():
    valid_blocks = []
    used_pairs = set()
    
    
    for block in BLOCKS:
        print(f"\nValidate this block: {block}")

        PoW1 = input("Enter first ProofOfWork  :").strip()
        PoW2 = input("Enter second ProofOfWork :").strip()

        try:
            PoW1_bytes = bytes.fromhex(PoW1)
            PoW2_bytes = bytes.fromhex(PoW2)

            if len(PoW1_bytes) != 16 or len(PoW2_bytes) != 16:
                print("Invalid Pow! must be 16 bytes")
                continue

            if (PoW1, PoW2) in used_pairs or (PoW2, PoW1) in used_pairs:
                print("These have already been used together!")
                continue
            
            used_pairs.add((PoW1, PoW2))
            

            enc1 = encrypt_with_tea(bytes.fromhex(block), PoW1_bytes)
            enc2 = encrypt_with_tea(bytes.fromhex(block), PoW2_bytes)

            if enc1 == enc2 and PoW1 != PoW2:
                valid_blocks.append(block)
                print("Good job validating the block!")
            else:
                print("Not Quite there!")
                continue

        except ValueError:
            print("Invalid input! Enter valid proofofwork.")
            continue

    if len(valid_blocks) == 6:
        print(f"Wait Noooooooooo: {FLAG}")
    else:
        print("Naaah, you need 6 valid blocks!")
        sys.exit(1)

if __name__ == "__main__":
    print(WELCOME_MSG)
    validate_blocks()

