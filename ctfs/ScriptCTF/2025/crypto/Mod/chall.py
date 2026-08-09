#!/usr/local/bin/python3
import os
secret = int(os.urandom(32).hex(),16)
print("Welcome to Mod!")
num=int(input("Provide a number: "))
print(num % secret)
guess = int(input("Guess: "))
if guess==secret:
    print(open('flag.txt').read())
else:
    print("Incorrect!")
