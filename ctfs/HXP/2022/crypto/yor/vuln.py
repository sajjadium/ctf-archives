#!/usr/bin/env python3
import random

greets = [
        "Herzlich willkommen! Der Schlüssel ist {0}, und die Flagge lautet {1}.",
        "Bienvenue! Le clé est {0}, et le drapeau est {1}.",
        "Hartelĳk welkom! De sleutel is {0}, en de vlag luidt {1}.",
        "ようこそ！鍵は{0}、旗は{1}です。",
        "歡迎！鑰匙是{0}，旗幟是{1}。",
        "Witamy! Niestety nie mówię po polsku...",
    ]

flag = open('flag.txt').read().strip()
assert set(flag.encode()) <= set(range(0x20,0x7f))

key = bytes(random.randrange(256) for _ in range(16))
hello = random.choice(greets).format(key.hex(), flag).encode()

output = bytes(y | key[i%len(key)] for i,y in enumerate(hello))
print(output.hex())

