#!/usr/bin/env python3

FLAG = "CyberErudites{fake_flag}"
BLACKLIST = '"%&\',-/_:;@\\`{|}~*<=>[] \t\n\r'

def check(s):
    return all(ord(x) < 0x7f for x in s) and all(x not in s for x in BLACKLIST)

def safe_eval(s, func):
    if not check(s):
        print("Input is bad")
    else:
        try:
            print(eval(f"{func.__name__}({s})", {"__builtins__": {func.__name__: func}, "flag": FLAG}))
        except:
            print("Error")

if __name__ == "__main__":
    safe_eval(input("Input : "), type)
