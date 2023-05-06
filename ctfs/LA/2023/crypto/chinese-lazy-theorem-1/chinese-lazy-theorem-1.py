#!/usr/local/bin/python3

from Crypto.Util.number import getPrime
from Crypto.Random.random import randint

p = getPrime(512)
q = getPrime(512)
n = p*q

target = randint(1, n)

used_oracle = False

print(p)
print(q)

print("To quote Pete Bancini, \"I'm tired.\"")
print("I'll answer one modulus question, that's it.")
while True:
    print("What do you want?")
    print("1: Ask for a modulus")
    print("2: Guess my number")
    print("3: Exit")
    response = input(">> ")

    if response == "1":
        if used_oracle:
            print("too lazy")
            print()
        else:
            modulus = input("Type your modulus here: ")
            modulus = int(modulus)
            if modulus <= 0:
                print("something positive pls")
                print()
            else:
                used_oracle = True
                print(target%modulus)
                print()
    elif response == "2":
        guess = input("Type your guess here: ")
        if int(guess) == target:
            with open("flag.txt", "r") as f:
                print(f.readline())
        else:
            print("nope")
        exit()
    else:
        print("bye")
        exit()
