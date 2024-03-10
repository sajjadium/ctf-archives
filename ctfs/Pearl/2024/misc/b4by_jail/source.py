#!/usr/local/bin/python
import time
flag="pearl{f4k3_fl4g}"
blacklist=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~`![]{},<>/123456789")
def banner():
    file=open("txt.txt","r").read()
    print(file)
def check_blocklist(string):
    for i in string:
        if i in blacklist:
            return(0)
    return(1)
def main():
    banner()
    cmd=input(">>> ")
    time.sleep(1)
    if(check_blocklist(cmd)):
        try:
            print(eval(cmd))
        except:
            print("Sorry no valid output to show.")
    else:
        print("Your sentence has been increased by 2 years for attempted escape.")

main()
