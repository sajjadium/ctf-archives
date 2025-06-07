#!/usr/bin/env sage
import os, json, random
from hashlib import md5
from Crypto.Cipher import DES

FLAG = os.getenv("FLAG", "bi0sctf{fake_flag}")
randomness = os.urandom(16)
SECRET = os.urandom(16)
server_seed = os.urandom(4)

def gen_rand(user_seed, server_seed):
    return DES.new(user_seed + server_seed, DES.MODE_ECB).encrypt(randomness)

def encode(data):
    P.<x> = ComplexField(128)[]
    poly = 0
    for i in range(len(data)):
        poly += data[i] * x ^ i
    return poly.roots()[1][0]

seen_seeds = set()

for i in range(3):
    try:
        user_input = json.loads(input())
        option = user_input.get("option")
        if option == "get_secret":
            user_seed = os.urandom(4)
            seen_seeds.add(user_seed)
            encoded_secret = encode(SECRET)
            error = encode(gen_rand(user_seed, server_seed))
            print(json.dumps({"encoded_secret": str(encoded_secret + error), "user_seed": user_seed.hex()}))
        elif option == "encode":
            data = bytes.fromhex(user_input.get("data"))
            user_seed = bytes.fromhex(user_input.get("user_seed"))
            if len(data) != 16 or len(user_seed) != 4:
                print(json.dumps({"error": "Invalid input"}))
                continue
            if user_seed in seen_seeds:
                print(json.dumps({"error": "Seed already used"}))
                continue
            seen_seeds.add(user_seed)
            encoded_data = str(encode(data) + encode(gen_rand(user_seed, server_seed)))
            print(json.dumps({"encoded_data": encoded_data}))
        elif option == "verify":
            user_secret = bytes.fromhex(user_input.get("user_secret"))
            if user_secret == SECRET:
                print(json.dumps({"flag": FLAG}))
            else:
                print(json.dumps({"error": "Invalid secret"}))
        else:
            print(json.dumps({"error": "Invalid option"}))
    except Exception as e:
        print(json.dumps({"error": "Invalid input"}))
        continue