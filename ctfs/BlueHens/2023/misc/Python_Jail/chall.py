#!/usr/bin/env python 

blacklist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

security_check = lambda s: any(c in blacklist for c in s) and s.count('_') < 50

def main():
    while True: 
        cmds = input("> ")
        if security_check(cmds):
            print("nope.")
        else:
            exec(cmds, {'__builtins__': None}, {})
    

if __name__ == "__main__":
    main()
