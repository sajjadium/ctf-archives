#!/usr/local/bin/python3

import json
import random
import numpy as np

FLAG = open("flag.txt").read()

BANNER = """
 _____                                                            _____ 
( ___ )----------------------------------------------------------( ___ )
 |   |                                                            |   | 
 |   |                                                            |   | 
 |   |     $$$$$$$\\  $$\\   $$\\ $$\\       $$$$$$$$\\  $$$$$$\\       |   | 
 |   |     $$  __$$\\ $$ |  $$ |$$ |      $$  _____|$$  __$$\\      |   | 
 |   |     $$ |  $$ |$$ |  $$ |$$ |      $$ |      $$ /  \\__|     |   | 
 |   |     $$$$$$$  |$$ |  $$ |$$ |      $$$$$\\    \\$$$$$$\\       |   | 
 |   |     $$  __$$< $$ |  $$ |$$ |      $$  __|    \\____$$\\      |   | 
 |   |     $$ |  $$ |$$ |  $$ |$$ |      $$ |      $$\\   $$ |     |   | 
 |   |     $$ |  $$ |\\$$$$$$  |$$$$$$$$\\ $$$$$$$$\\ \\$$$$$$  |     |   | 
 |   |     \\__|  \\__| \\______/ \\________|\\________| \\______/      |   | 
 |   |                                                            |   | 
 |___|                                                            |___| 
(_____)----------------------------------------------------------(_____)
"""

def rotate_left(data):
    upper = data << 1
    lower = np.roll(data, -1) >> 7
    
    return upper | lower

def rotate_right(data):
    lower = data >> 1
    upper = np.roll(data, 1) << 7
    
    return upper | lower

def rule(data):
    left = rotate_left(data)
    right = rotate_right(data)

    return ~((left & right & data) | (~left & ~right & ~data) | (~left & right & ~data))

def main():
    print(BANNER)
    print("\nGive me a list of bytes, and guess what it becomes!")
    print("Rules:")
    print("1. All war is based on deception.\n")

    print("Enter the bytes:")
    user_input = input("> ")
    arr = json.loads(user_input)
    if not isinstance(arr, list) or not all(isinstance(x, int) for x in arr):
        print("Invalid input")
        return

    data = np.array(arr, dtype=np.uint8)
    if len(data) < 1024:
        print("Too short")
        return

    print("Make a guess:")
    user_guess = input("> ")
    user_guess = user_input
    guess = np.array(json.loads(user_guess), dtype=np.uint8)

    if guess.shape != data.shape:
        print("Invalid guess")
        return

    print("Checking guess...")
    num_rounds = random.randint(100, 16000)
    for i in range(num_rounds):
        data = rule(data)
        if not np.any(data):
            print("All zeroes!")
            return

    if np.array_equal(guess, data):
        print("Correct!")
        print(f"Here is your flag: {FLAG}")
    else:
        print("Incorrect!")

if __name__ == "__main__":
    try:
        main()
    except:
        print("Error")
