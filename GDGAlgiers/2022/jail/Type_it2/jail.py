#!/usr/bin/env python3

with open("./flag.txt") as f:
    FLAG = f.read().strip()

BLACKLIST = '"%&\',-/_:;@\\`{|}~*<=>[] \t\n\r\x0b\x0c'

OPEN_LIST = '(['
CLOSE_LIST = ')]'

class BadInput(Exception):
    pass

def check_balanced(s):
    stack = []
    for i in s:
        if i in OPEN_LIST:
            stack.append(i)
        elif i in CLOSE_LIST:
            pos = CLOSE_LIST.index(i)
            if ((len(stack) > 0) and
                (OPEN_LIST[pos] == stack[len(stack)-1])):

                stack.pop()
            else:
                return False
    return len(stack) == 0

def check(s):
    return all(ord(x) < 0x7f for x in s) and all(x not in s for x in BLACKLIST) and check_balanced(s)

def safe_eval(s, func):
    if not check(s):
        print("Input is bad")
    else:
        try:
            print(eval(f"{func.__name__}({s})", {"__builtins__": {func.__name__: func}, "flag": FLAG}))
        except:
            print("Error")

if __name__ == "__main__":
    while True :
        inp = input("Input : ")
        if inp == "EXIT":
            exit()
        safe_eval(inp, type)
