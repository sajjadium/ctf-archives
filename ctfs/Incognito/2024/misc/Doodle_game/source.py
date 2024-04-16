#!/usr/bin/python
import time
import unicodedata

blacklist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789[]{}<>/_'!"

def isSafe(cmd):
    for i in cmd:
        if i in blacklist:
            return(0)
    return(1)

def main():
    cmd = input(">> ")
    normalized_cmd = unicodedata.normalize('NFKD', cmd).encode('ASCII', 'ignore').decode()
    if(isSafe(normalized_cmd)):
        try:
            if(eval(normalized_cmd) == 17592186044416):
                print(open("flag").readline())
            else:
                print(eval(normalized_cmd))
        except:
            print("An exception occurred")

    else:
        print("Not allowed!")

main()
