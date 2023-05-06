#!/usr/bin/env python3

import sys
from Crypto.Util.number import *
import time

MEMSIZE = 2**16
REGNAMES = ["r%d"%i for i in range(16)]+['rip']
DEBUG = 0

def prd(*args):
    if DEBUG:
        print(*args)

class MemoryException(Exception):
    pass

class Memory():
    def __init__(self, size=MEMSIZE, mem=None, rnames=REGNAMES):
        if mem is not None:
            self.size = mem.size
            self.regs = {k:mem.regs[k] for k in mem.regs}
            self.ram = {k:mem.ram[k] for k in mem.ram}
            self.regs['rip'] = 0
        else:
            self.size = size
            self.regs = {r:0 for r in rnames}
            self.ram = {}

    def setRam(self, addr, val):
        if type(addr) != int:
            raise MemoryException("Attempting to access invalid memory address "+str(addr))
        if addr < 0 or addr >= self.size:
            raise MemoryException("Memory "+str(addr)+" out of bounds!")
        self.ram[addr] = val

    def getRam(self, addr):
        if type(addr) != int:
            raise MemoryException("Attempting to access invalid memory address "+str(addr))
        if addr < 0 or addr >= self.size:
            raise MemoryException("Memory "+str(addr)+" out of bounds!")
        if addr in self.ram:
            return self.ram[addr]
        self.ram[addr] = 0
        return 0

    def getVal(self, val):
        if type(val) != str or len(val) == 0:
            raise MemoryException("Bad value "+str(val)+" recieved!")
        if val.isdigit():
            return int(val)
        if val in self.regs:
            return self.regs[val]
        if val[0] == '[' and val[-1] == ']':
            return self.getRam(self.getVal(val[1:-1]))
        if val[0] == '"' and val[-1] == '"':
            return val[1:-1]
        if val[0] == "'" and val[-1] == "'":
            return val[1:-1]
        raise MemoryException("Bad value "+str(val)+" recieved!")

    def assign(self, loc, val):
        if type(loc) != str or len(loc) == 0:
            raise MemoryException("Bad location "+str(loc)+" recieved!")
        if loc in self.regs:
            self.regs[loc] = val
            return
        if loc[0] == '[' and loc[-1] == ']':
            self.setRam(self.getVal(loc[1:-1]), val)

    def rip(self):
        return self.regs['rip']

    def inc_rip(self):
        self.regs['rip'] += 1

class VM():
    def __init__(self, program='', memory=None):
        self.program = self.parseStr(program)
        if memory is not None:
            self.mem = Memory(mem=memory)
        else:
            self.mem = Memory(size=MEMSIZE)

        self.insns_map = {"add": self.add,
                          "sub": self.sub, 
                          "mult": self.mult, 
                          "div": self.div, 
                          "mod": self.mod,
                          "xor": self.xor, 
                          "and": self.andd,
                          "or": self.orr,
                          "rev": self.rev,
                          "mov": self.mov,
                          "strint": self.strint,
                          "intstr": self.intstr,
                          "pr": self.pr,
                          "readstr": self.readstr,
                          "readint": self.readint,
                          "j": self.jump,
                          "jnz": self.jnz,
                          "jz": self.jz,
                          "jl": self.jl,
                          } # also labels

    def quit(self, msg='', exitcode=1, test=False):
        if exitcode != 0:
            print("Error running line '", self.c_insn(), "' at insn pointer", self.mem.rip())
        if msg == '':
            print("Quitting...")
        else:
            print(msg)
        exit(exitcode)

    def parseStr(self, s):
        return [line.strip() for line in s.split('\n')]

    def parseInsn(self, insn):
        args = insn.split("#")[0].strip().split(" ")
        cmd = args[0]
        rest = " ".join(args[1:]).strip().split(", ")
        return [cmd]+rest

    def c_insn(self):
        return self.program[self.mem.rip()]

    def run(self):
        try:
            while self.mem.rip() < len(self.program):
                prd("Executing '"+self.c_insn()+"' at insn_pointer "+str(self.mem.rip()))
                self.execute_insn(self.c_insn())
                self.mem.inc_rip()
        except MemoryException as e:
            self.quit(str(e))
        except Exception as e:
            print("Unknown error occurred.")
            if DEBUG:
                raise e
            self.quit()

    def execute_insn(self, insn):
        if insn == '' or insn[-1] == ':' or insn[0] == "#":
            return
        args = self.parseInsn(insn)
        prd(args)
        self.insns_map[args[0]](*args[1:])

    def setRam(self, addr, val):
        return self.mem.setRam(addr, val)

    def getRam(self, addr):
        return self.mem.getRam(addr)

    def getVal(self, val):
        return self.mem.getVal(val)

    def assign(self, loc, val):
        return self.mem.assign(loc, val)

    def reset(self):
        self.mem = Memory()

    def add(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) != type(a2):
            a1 = str(a1)
            a2 = str(a2)
        self.assign(args[0], a1+a2)

    def sub(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) != int or type(a2) != int:
            self.quit("sub args not int!")
        self.assign(args[0], a1-a2)

    def mult(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) == str or type(a2) == str:
            self.quit("Both mult args are strings!")
        self.assign(args[0], a1*a2)

    def div(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) != int or type(a2) != int:
            self.quit("div args not int!")
        self.assign(args[0], a1//a2)

    def mod(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) != int or type(a2) != int:
            self.quit("mod args not int!")
        self.assign(args[0], a1%a2)

    def andd(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) != int or type(a2) != int:
            self.quit("and args not int!")
        self.assign(args[0], a1&a2)

    def orr(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) != int or type(a2) != int:
            self.quit("or args not int!")
        self.assign(args[0], a1|a2)

    def xor(self, *args):
        a1 = self.getVal(args[1])
        a2 = self.getVal(args[2])
        if type(a1) == int and type(a2) == int:
            self.assign(args[0], a1^a2)
        else:
            a1 = long_to_bytes(a1).decode() if type(a1) == int else a1
            a2 = long_to_bytes(a2).decode() if type(a2) == int else a2
            self.assign(args[0], self.xorstr(a1, a2))

    def xorstr(self, s1, s2):
        l = max(len(s1), len(s2))
        s1 = s1.encode()
        s2 = s2.encode()
        ret = ''
        for i in range(l):
            ret += chr(s1[i%len(s1)]^s2[i%len(s2)])
        return ret

    def readint(self, *args):
        try:
            self.assign(args[0], int(input()))
        except ValueError as e:
            self.quit("Bad int input!")

    def readstr(self, *args):
        self.assign(args[0], input())

    def pr(self, *args):
        print(self.getVal(args[0]), end='', flush=True)

    def strint(self, *args):
        a1 = self.getVal(args[1])
        if type(a1) != str:
            self.quit("Attempting to convert non-string to int!")
        self.assign(args[0], bytes_to_long(bytes([ord(i) for i in a1])))

    def intstr(self, *args):
        a1 = self.getVal(args[1])
        if type(a1) != int:
            self.quit("Attempting to convert non-int to string!")
        try:
            b = bytes.fromhex(hex(a1)[2:])
        except ValueError as e:
            if 'non-hexadecimal' not in str(e):
                raise e
            b = bytes.fromhex('0'+hex(a1)[2:])
        self.assign(args[0], ''.join([chr(i) for i in b]))

    def revint(self, i):
        sign = 0 if not i else (1 if i>0 else -1)
        return sign*int(str(abs(i))[::-1])

    def rev(self, *args):
        a1 = self.getVal(args[1])
        if type(a1) == int:
            ret = self.revint(a1)
        else:
            ret = a1[::-1]
        self.assign(args[0], ret)

    def mov(self, *args):
        self.assign(args[0], self.getVal(args[1]))

    def jump(self, *args):
        for i, insn in enumerate(self.program):
            if insn == args[0]+':':
                self.assign('rip', i)
                return
        self.quit("Could not find label "+args[0]+"!")

    def jz(self, *args):
        if self.getVal(args[0]) == 0:
            self.jump(args[1])

    def jnz(self, *args):
        if self.getVal(args[0]) != 0:
            self.jump(args[1])

    def jl(self, *args):
        if self.getVal(args[0]) < self.getVal(args[1]):
            self.jump(args[2])

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        self.quit("Usage: ./icicle.py [filename]", 0)

    with open(sys.argv[1], 'r') as f:
        vm = VM(program=f.read())
        vm.run()