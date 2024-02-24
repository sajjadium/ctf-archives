#!/bin/python3

# THIS WOULD BE A TEST INTERPRETER PROGRAMME FOR BRAINF*CK THAT YOU CAN MODIFY AND USE
# TO TEST OUT YOUR SOLUTIONS TO THE GIVEN PROBLEMS
# THIS IS SIMILAR TO THE REMOTE VERSION BUT IS NOT THE SAME AND THE REMOTE HAS WAY MORE FUNCTIONALITY THAN THE FOLLOWING CODE

from time import *
import sys
import os

TAPESIZE = 30000

# ALLOCATING TAPE
# TAPE IS INITIALISED TO ZERO FOR EVERY RUN
tape = [0 for i in range (TAPESIZE)]

# SETTING AN INSTRUCTION PTR
dp   = 0
pc   = 0

loopstack = []

def banner():
    os.system("clear")
    print(
        '''
▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
\u258f  ___ ___    _   ___ _  _ ___                                 \u258f
\u258f | _ ) _ \  /_\ |_ _| \| | __|/\_                             \u258f
\u258f | _ \   / / _ \ | || .` | _|>  <                             \u258f
\u258f |___/_|_\/_/ \_\___|_|\_|_|  \/                              \u258f
\u258f  ___ ___  ___   ___ ___    _   __  __ __  __ ___ _  _  ___   \u258f
\u258f | _ \ _ \/ _ \ / __| _ \  /_\ |  \/  |  \/  |_ _| \| |/ __|  \u258f
\u258f |  _/   / (_) | (_ |   / / _ \| |\/| | |\/| || || .` | (_ |  \u258f
\u258f |_| |_|_\\\___/ \___|_|_\/_/ \_\_|  |_|_|  |_|___|_|\_|\___|  \u258f
\u258f                                                              \u258f
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔'''
    )
    
# BASIC CHECKS FOR OOB ARRAY ACCESS
def checkdp():
    if (dp < 0 or dp > (TAPESIZE-1)):
        print("               [ERROR]                ")
        print("----DATA-POINTER-WENT-OUT-THE-TAPE----")
        exit(-1)

def parantherr():
    print("               [ERROR]                ")
    print("-------UNMATCHED-LOOP-OPERATOR--------")
    exit(-1)

def findmatch(code,pc,p):
    tmp = []
    offset = 1 if p == "[" else -1
    idx = pc + offset
    ptype = {"[":"]","]":"["}
    while(idx < len(code) and idx >= 0):
        if(code[idx] == p):
            tmp.append(idx)
        if(code[idx] == ptype[p]):
            if(len(tmp)):
                tmp.pop(-1)
            else:
                return idx
        idx += offset
    return parantherr()

# READING IN THE CODE WHICH IS TO BE RUN
def readincode(nbytes : int):
    code = ""
    for i in range (nbytes):
        ins = sys.stdin.read(1)
        if(type(ins) == bytes):
            ins = ins.decode()
        code += ins
        if "\n" in code:
            break
    end = code.find("\n")
    return code[0:end]

# JUST PRETTY PRINTS THE TAPE FOR YOU
def debug():
    os.system("clear")
    print("")
    print("▕",end="")
    for i in range (51):
        print("▔▔",end="")
    print("▔▏")
    if(dp>=5):
        print("▕  ",end="")
        for i in range (10):
            if(i-5==0):
                print((f"\033[1;31m[\033[0m{dp+i-5}\033[1;31m]\033[0m".center(29," "))," ",end="")
                continue
            else: print((f"[{dp+i-5}]".center(7," "))," ",end="")
        print(" <<  {dp}  ▏")
        print("▕ -",end="")
        for i in range (10):
            print("---------",end="")
        print("           ▏")
        print("▕ |",end="")
        for i in range (10):
            if(i-5==0):
                print(((f"\033[1;31m{tape[dp+i-5]}\033[0m").center(18," ")),"|",end="")
                continue
            print((f"{tape[dp+i-5]}".center(7," ")),"|",end="")
        print(" << {tape} ▏")
        print("▕  ",end="")
        for i in range (50):
            print("  ",end="")
        print(" ▏")
        print(" ",end="")
        for i in range (51):
            print("▔▔",end="")
        print("▔")
        sleep(0.1)
    else:
        print("▕  ",end="")
        for i in range (10):
            if(i==dp):
                print((f"\033[1;31m[\033[0m{dp}\033[1;31m]\033[0m".center(29," "))," ",end="")
                continue
            print((f"[{i}]".center(7," "))," ",end="")
        print(" <<  {dp}  ▏")
        print("▕ -",end="")
        for i in range (10):
            print("---------",end="")
        print("           ▏")
        print("▕ |",end="")
        for i in range (10):
            if(i==dp):
                print(((f"\033[1;31m{tape[dp]}\033[0m").center(18," ")),"|",end="")
                continue
            print((f"{tape[i]}".center(7," ")),"|",end="")
        print(" << {tape} ▏")
        print("▕  ",end="")
        for i in range (50):
            print("  ",end="")
        print(" ▏")
        print(" ",end="")
        for i in range (51):
            print("▔▔",end="")
        print("▔")
        sleep(0.1)

# BRAINF_CK INTERPRETER BUT WITHOUT THE . AND , INSTRUCTIONS
def run(code):
    global pc,dp
    pc = 0
    while (pc != len(code)):
        debug()
        if(code[pc] == ">"):
            dp += 1
            checkdp()
            pc += 1
            continue
        if(code[pc] == "<"):
            dp -= 1
            checkdp()
            pc += 1
            continue
        if(code[pc] == "+"):
            tape[dp] = (tape[dp] + 1) % 0x100
            pc += 1
            continue
        if(code[pc] == "-"):
            tape[dp] = (tape[dp] - 1) % 0x100
            pc += 1
            continue
        if(code[pc] == "["):
            if(tape[dp] == 0):
                idx = findmatch(code,pc,"[")
                pc = idx + 1
                continue
            else:
                loopstack.append(pc)
                pc += 1
                continue
        if(code[pc] == "]"):
            if(tape[dp] != 0):
                if(len(loopstack)):
                    pc = loopstack.pop(-1)
                    continue
            else:
                if(len(loopstack)):
                    loopstack.pop(-1)
                else:
                    parantherr()
                pc += 1
                continue
        else:
            pc += 1
            continue

def test():
    print("▍>> DATA POINTER AT -",dp)
    print("▍>> INPUT YOUR CODE : ",end="",flush=True)
    code = readincode(0xff)
    run(code)
    debug()

def main():
    banner()
    test()

if __name__== \
    "__main__":
    main()
