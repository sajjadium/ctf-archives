#!/usr/local/bin/python
import random

flag = open("flag.txt").read().strip()
r = random.randint(1, 1000)
guessed = False
for i in range(10):
    guess = int(input("Guess a number from 1 to 1000: "))
    if guess > r:
        print("Too high")
    elif guess < r:
        print("Too low")
    else:
        guessed = True
        break
if guessed == True:
    print(f"You won, the flag is {flag}")
else:
    print(f"You lost, the number was {r}")
