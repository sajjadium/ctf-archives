#!/usr/bin/env python3

import spy
from secret import flag

print("Lets play a simple game!");
print("");
print("I'll give you a list of numbers, and you need to spy with");
print("your little eye which two numbers in the list are swapped");
print("as fast as possible!");
print("");

while True:
    print("--- New Game ---")
    print()

    mode = input("Easy or Hard? ")
    if mode.strip().lower() == "hard":
        result = spy.hard()
    elif mode.strip().lower() == "easy":
        result = spy.easy()
    else:
        break

    if result == "REWARD":
        print("Wow, you are really good. You deserve a reward!")
        print("Here is a flag for you troubles:", flag)
    elif result == "MOTIVATE":
        print("Not too shabby. Try out the hard mode next!")
    else:
        print("Sorry, too slow. Better luck next time!")
    print()
