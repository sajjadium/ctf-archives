#!/usr/local/bin/python3 -u
from Crypto.Util.number import long_to_bytes

def main():
    print("Welcome to the brig. There is no escape, you may as well just give up")
    print("I'll be a kind captain and let you play with two symbols...\n")
    inp = input('> ')
    if len(inp) != 2:
        print("I see you smuggleing contraband in!")
        return 1
    ok_chars = set(inp)
    print("Hahaha! You really think you can escape with that? I'd like to see you try!")
    inp = input('> ')
    if not set(inp) <= ok_chars:
        print("You don't have that tool")
        return 1
    if len(inp) >= 2**12:
        print("You took too long! We have already arrived")
        return 1
    try:
        print(eval(long_to_bytes(eval(inp))))
    except:
        print("What are you trying to do there?")
    
    
if __name__ == "__main__":
    main()
