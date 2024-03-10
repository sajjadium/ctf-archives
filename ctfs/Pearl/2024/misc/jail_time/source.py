#!/usr/local/bin/python
import blackbox as blackbox
import time
flag="pearl{j4il_time}"

def banner():
    file=open("txt.txt","r").read()
    print(file)
def main():
    banner()
    cmd=input(">>> ")
    time.sleep(2)
    cmd=blackbox.normalise(cmd)
    if(blackbox.check_blocklist(cmd)):
        try:
            print(eval(eval(cmd)))
        except:
            print("Sorry no valid output to show.")
    else:
        print("Your sentence has been increased by 2 years for attempted escape.")
main()