#!/usr/bin/env python3

import sys
from PIL import Image
import numpy as np

class Stack(list):
    def push(self, x):
        self.append(x)

    def peek(self):
        return self[-1]

stack = Stack([])
program = []
register = 0
insn_pointer = 0

DEBUG = 0

def robinify(im):
    tiles = [im[x:x+128,y:y+128,0:4] for x in range(0,im.shape[0],128) for y in range(0,im.shape[1],128)]
    R = np.asarray(Image.open("robin.roo"))
    O = np.asarray(Image.open("oreos.roo"))
    B = np.asarray(Image.open("blind.roo"))
    I = np.asarray(Image.open("imag.roo"))
    N = np.asarray(Image.open("nobooli.roo"))
    d = list(zip([R,O,B,I,N], "robin"))

    ret = ''
    for c in tiles:
        for pair in d:
            if np.all(pair[0]==c):
                ret += pair[1]
                break
    return ret

def step():
    global insn_pointer
    insn = c_insn()
    if DEBUG:
        print(insn, program[insn_pointer+1], "@", insn_pointer)
    eval(insn+"()")

def run(prog):
    global insn_pointer, program
    for ch in prog:
        if ch not in "robin":
            print("Syntax Error")
            exit(1)

    if len(prog) % 5 != 0:
        print("Syntax Error")

    program = [prog[i:i+5] for i in range(0, len(prog), 5)]
    try:
        while insn_pointer < len(program):
            step()
            insn_pointer += 1
            if DEBUG:
                print(stack)
    except Exception as e:
        print("Fatal Error.")
        raise e
    print()
    print(stack)

def c_insn():
    return program[insn_pointer]

def robin():
    global insn_pointer
    insn_pointer += 1
    toPush = c_insn()
    if toPush == "rinin":
        stack.push(register)
    else:
        words = parseDigit(toPush)
        toPush = 0
        for i in range(words):
            insn_pointer += 1
            toPush += parseDigit(c_insn())
            toPush *= 27
        stack.push(toPush//27)
    
def parseDigit(s):
    return int(s.replace('o', '0').replace('b', '1').replace('i', '2')[1:-1], 3)

def rboin():
    stack.pop()

def riobn():
    stack.push(stack.pop()+stack.pop())

def rooon():
    stack.push(stack.pop()-stack.pop())

def riibn():
    stack.push(stack.pop()*stack.pop())

def riion():
    stack.push(stack.pop()//stack.pop())

def ribon():
    stack.push(stack.pop()%stack.pop())

def ronon():
    stack.push(stack.pop()&stack.pop())

def roion():
    stack.push(stack.pop()|stack.pop())

def roibn():
    stack.push(stack.pop()^stack.pop())

def riiin():
    x = stack.pop()
    stack.push(x)
    stack.push(x)

def rioin():
    x = stack.pop()
    y = stack.pop()
    stack.push(x)
    stack.push(y)

def rinin():
    global register
    register = stack.pop()

def rbiin():
    print(chr(stack.pop()), end='', flush=True)

def rboon():
    print(stack.pop(), end='', flush=True)

def rnbon():
    global insn_pointer
    insn_pointer += 1

def rioon():
    global insn_pointer
    insn_pointer += 1
    for i, word in enumerate(program):
        if word == "rnbon":
            if i != len(program)-1 and program[i+1] == c_insn():
                insn_pointer = i+1
                return
    print("Label not found!")
    raise RuntimeError

def rbion():
    global insn_pointer
    if stack.peek():
        rioon()
    else:
        insn_pointer += 1

def ribbn():
    global insn_pointer
    retval = stack.pop()
    insn_pointer = stack.pop()
    if DEBUG:
        print("returning to", insn_pointer)
    stack.push(retval)

def roiin():
    global insn_pointer
    arg = stack.pop()
    stack.push(insn_pointer+1)
    stack.push(arg)
    rioon()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./roolang.py [filename.roo]")
        exit()

    if sys.argv[1].split('.')[-1] != "roo":
        print("Invalid file format!")
        exit()

    with Image.open(sys.argv[1]) as f:
        print("Parsing...")
        program = robinify(np.asarray(f))
        print("Running...")
        run(program)
        print("Finished execution.")
