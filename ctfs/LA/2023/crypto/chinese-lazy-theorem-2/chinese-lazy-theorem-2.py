#!/usr/local/bin/python3

from Crypto.Util.number import getPrime
from Crypto.Random.random import randint

p = getPrime(512)
q = getPrime(512)
n = p*q*2*3*5

target = randint(1, n)

oracle_uses = 0

print(p)
print(q)

print("This time I'll answer 2 modulus questions and give you 30 guesses.")
while True:
    print("What do you want?")
    print("1: Ask for a modulus")
    print("2: Guess my number")
    print("3: Exit")
    response = input(">> ")

    if response == "1":
        if oracle_uses == 2:
            print("too lazy")
            print()
        else:
            modulus = input("Type your modulus here: ")
            modulus = int(modulus)
            if modulus <= 0:
                print("something positive pls")
                print()
            elif modulus > max(p, q):
                print("something smaller pls")
                print()
            else:
                oracle_uses += 1
                print(target%modulus)
                print()
    elif response == "2":
        for _ in range(30):
            guess = input("Type your guess here: ")
            if int(guess) == target:
                with open("flag.txt", "r") as f:
                    print(f.readline())
                    exit()
            else:
                print("nope")
        exit()
    else:
        print("bye")
        exit()
