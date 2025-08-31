#!/usr/local/bin/python3
import random; FLAG = open("flag.txt", "rb").read(); print("welcome to oooo")
while True: print(bytes(a^b for a, b in zip(FLAG, random.sample(range(0, 256), k=len(FLAG)))).hex() if input() != "exit" else exit())