import sys
import os
import random
import struct
X13 = 1024*1024
X14 = 10
X15 = 2000
X16 = 55 
class Instruction:
    op = None
    imm = 0
    X11 = None
    X12 = None
    dsp = None
    X08 = None
    X10 = 0
    X02 = 0
    def __init__(self, tstr):
        def X06(tt):
            if tt.startswith("0x"):
                try:
                    v = int(tt, 16)
                except ValueError:
                    assert False
            else:
                try:
                    v = int(tt)
                except ValueError:
                    assert False
            assert v>=0
            assert v<pow(2,32)
            return v
        def X17_X08(tt):
            try:
                v = int(tt)
            except ValueError:
                assert False
            assert v>-1000
            assert v<1000
            return v
        def X07(tt):
            assert len(tt) == 2
            assert tt[0] == "r"
            try:
                v = int(tt[1])
            except ValueError:
                assert False
            assert v>=0
            assert v<X14
            return v
        def X17_memory(tt):
            try:
                v = int(tt)
            except ValueError:
                assert False
            assert v>=0
            assert v<X13
            return v
        assert len(tstr)<100
        sstr = tstr.split()
        assert len(sstr)>=1
        assert len(sstr)<=4
        if len(sstr) == 1:
            t_op = sstr[0]
            assert t_op in ["halt", "time", "magic", "reset"]
            self.op = t_op
        elif len(sstr) == 2:
            t_op, t_1 = sstr
            assert t_op in ["jmp", "jmpz"]
            self.op = t_op
            if self.op == "jmp":
                self.X08 = X17_X08(t_1)
            elif self.op == "jmpz":
                self.X08 = X17_X08(t_1)
            else:
                assert False
        elif len(sstr) == 3:
            t_op, t_1, t_2 = sstr
            assert t_op in ["mov", "movc", "jmpg", "add", "sub", "mul", "and", "or", "xor"]
            self.op = t_op
            if self.op == "mov":
                self.X11 = X07(t_1)
                self.X12 = X07(t_2)
            elif self.op in ["add", "sub", "mul", "and", "or", "xor"]:
                self.X11 = X07(t_1)
                self.X12 = X07(t_2)
            elif self.op == "movc":
                self.X11 = X07(t_1)
                self.imm = X06(t_2)
            elif self.op == "jmpg":
                self.X08 = X17_X08(t_2)
                self.X11 = X07(t_1)
            else:
                assert False
        elif len(sstr) == 4:
            t_op, t_1, t_2, t_3 = sstr
            assert t_op in ["movfrom", "movto"]
            self.op = t_op
            if self.op == "movfrom":
                self.X11 = X07(t_1)
                self.X10 = X17_memory(t_2)
                self.dsp = X07(t_3)
            elif self.op == "movto":
                self.X11 = X07(t_1)
                self.X10 = X17_memory(t_2)
                self.dsp = X07(t_3)
            else:
                assert False
        else:
            assert False
    def pprint(self):
        tstr = "%s %s %s %s %s %s" %            (self.op, 
            "None" if self.X11==None else "r%d"%self.X11,
            "None" if self.X12==None else "r%d"%self.X12,
            hex(self.imm), "None" if self.X08==None else self.X08, self.X10)
        return tstr
class Cpu:
    X05 = 0
    instructions = None
    X01 = None
    memory = None
    X02 = 0
    X03 = None
    X00 = 0
    X04 = None
    def __init__(self):
        self.instructions = []
        self.X03 = {}
        self.X04 = (random.randint(1,4200000000), random.randint(1,4200000000) , random.randint(1,4200000000), random.randint(1,4200000000))
        self.reset()
    def reset(self):
        self.X05 = 0
        self.X01 = [0 for r in range(X14)]
        self.memory = [0 for _ in range(X13)]
        self.X02 = 0
        for k in self.X03.keys():
            self.X03[k] = 0
        self.X00 += 1
    def load_instructions(self, tt):
        for line in tt.split("\n"):
            if "#" in line:
                line = line.split("#")[0]
            line = line.strip()
            if not line:
                continue
            self.instructions.append(Instruction(line))
            assert len(self.instructions) <= X16
    def run(self, debug=0):
        ins = self.instructions[0]
        for i,v in enumerate(self.X04):
            self.memory[i] = v
        while (self.X05>=0 and self.X05<len(self.instructions) and self.X00<4 and self.X02<20000):
            ins = self.instructions[self.X05]
            self.execute(ins)
    def execute(self, ins):
        self.X02 += 1
        if ins.op == "movc":
            self.X01[ins.X11] = ins.imm
            self.X05 += 1
        elif ins.op == "magic":
            if self.X00 == 2:
                if tuple(self.X01[0:4]) == self.X04:
                    with open("flag.txt", "rb") as fp:
                        cc = fp.read()
                    cc = cc.strip()
                    cc = cc.ljust(len(self.X01)*4, b"\x00")
                    for i in range(len(self.X01)):
                        self.X01[i] = struct.unpack("<I", cc[i*4:(i+1)*4])[0]
            self.X05 += 1
        elif ins.op == "reset":
            self.reset()
        elif ins.op == "halt":
            self.X05 = len(self.instructions)
        elif ins.op == "time":
            self.X01[0] = self.X02
            self.X05 += 1
        elif ins.op == "jmp":
            nt = self.X05 + ins.X08
            assert nt >=0 
            assert nt < len(self.instructions)
            self.X05 = nt
        elif ins.op == "jmpz":
            if self.X01[0] == 0:
                nt = self.X05 + ins.X08
                assert nt >=0 
                assert nt < len(self.instructions)
                self.X05 = nt
            else:
                self.X05 += 1
        elif ins.op == "jmpg":
            if self.X01[0] > self.X01[ins.X11]:
                nt = self.X05 + ins.X08
                assert nt >=0 
                assert nt < len(self.instructions)
                self.X05 = nt
            else:
                self.X05 += 1
        elif ins.op == "mov":
            self.X01[ins.X11] = self.X01[ins.X12]
            self.X05 += 1
        elif ins.op == "sub":
            v = self.X01[ins.X11] - self.X01[ins.X12]
            self.X01[ins.X11] = (v & 0xffffffff)
            self.X05 += 1
        elif ins.op == "add":
            v = self.X01[ins.X11] + self.X01[ins.X12]
            self.X01[ins.X11] = (v & 0xffffffff)
            self.X05 += 1
        elif ins.op == "mul":
            v = self.X01[ins.X11] * self.X01[ins.X12]
            self.X01[ins.X11] = (v & 0xffffffff)
            self.X05 += 1
        elif ins.op == "and":
            v = self.X01[ins.X11] & self.X01[ins.X12]
            self.X01[ins.X11] = (v & 0xffffffff)
            self.X05 += 1
        elif ins.op == "or":
            v = self.X01[ins.X11] | self.X01[ins.X12]
            self.X01[ins.X11] = (v & 0xffffffff)
            self.X05 += 1
        elif ins.op == "xor":
            v = self.X01[ins.X11] ^ self.X01[ins.X12]
            self.X01[ins.X11] = (v & 0xffffffff)
            self.X05 += 1
        elif ins.op == "movfrom":
            X09 = ins.X10 + self.X01[ins.dsp]
            X09 = X09 % len(self.memory)
            if X09 in self.X03:
                v = self.X03[X09]
                v = (v & 0xffffffff)
                self.X01[ins.X11] = v
                self.X05 += 1
            else:
                v = self.memory[X09]
                self.X03[X09] = v
                self.execute(ins)
        elif ins.op == "movto":
            X09 = ins.X10 + self.X01[ins.dsp]
            X09 = X09 % len(self.memory)
            if X09 in self.X03:
                del self.X03[X09]
            v = (self.X01[ins.X11] & 0xffffffff)
            self.memory[X09] = v
            self.X05 += 1
        else:
            assert False
        return 
    def pprint(self, debug=0):
        tstr = ""
        tstr += "%d> "%self.X05
        tstr += "[%d] "%self.X02
        tstrl = []
        for i,r in enumerate(self.X01):
            tstrl.append("r%d=%d"%(i,r))
        tstr += ",".join(tstrl)
        if debug>1:
            tstr += "\nM->"
            vv = []
            for i,v in enumerate(self.memory):
                if v!=0:
                    vv.append("%d:%d"%(i,v))
            tstr += ",".join(vv)
            tstr += "\nC->"
            tstr += repr(self.X03)
        return tstr
def main():
    print("Welcome to a very fast VM!")
    print("Give me your instructions.")
    print("To terminate, send 3 consecutive empty lines.")
    instructions = ""
    X18 = 0
    while True:
        line = input()
        if not line.strip():
            X18 += 1
        else:
            X18 = 0
        instructions += line + "\n"
        if X18 >= 3 or len(instructions) > X15:
            break
    c = Cpu()
    print("Parsing...")
    c.load_instructions(instructions)
    print("Running...")
    c.run()
    print("Done!")
    print("Registers: " + repr(c.X01))
    print("Goodbye.")
if __name__ == "__main__":
    sys.exit(main())