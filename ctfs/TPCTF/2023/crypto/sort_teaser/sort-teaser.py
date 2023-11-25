import re
from Crypto.Util.number import bytes_to_long
import random

letters=set(bytes(range(65,91)).decode())
class Command:
    def __init__(self, target_var, op, l, r=0):
        self.target_var = target_var
        self.op = op
        self.l = l if l in letters else int(l)
        self.r = r if r in letters else int(r)
    def __str__(self):
        return self.target_var+"="+str(self.l)+((self.op+str(self.r)) if self.op!="=" else "")
    __repr__=__str__

class Computation:
    def __init__(self):
        self.vars={x:0 for x in letters}
    
    def resolve_val(self,symbol):
        return self.vars[symbol] if type(symbol)==str else symbol
    
    def run(self,cmd):
        if cmd.op=='+':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)+self.resolve_val(cmd.r)
            if self.vars[cmd.target_var].bit_length()>100000:
                raise OverflowError
        elif cmd.op=='-':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)-self.resolve_val(cmd.r)
            if self.vars[cmd.target_var].bit_length()>100000:
                raise OverflowError
        elif cmd.op=='*':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)*self.resolve_val(cmd.r)
            if self.vars[cmd.target_var].bit_length()>100000:
                raise OverflowError
        elif cmd.op=='/':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)//self.resolve_val(cmd.r)
        elif cmd.op=='%':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)%self.resolve_val(cmd.r)
        elif cmd.op=='&':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)&self.resolve_val(cmd.r)
        elif cmd.op=='|':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)|self.resolve_val(cmd.r)
        elif cmd.op=='^':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)^self.resolve_val(cmd.r)
        elif cmd.op=='<':
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)<self.resolve_val(cmd.r))
        elif cmd.op=='>':
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)>self.resolve_val(cmd.r))
        elif cmd.op=='<=':
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)<=self.resolve_val(cmd.r))
        elif cmd.op=='>=':
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)>=self.resolve_val(cmd.r))
        elif cmd.op=='!=':
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)!=self.resolve_val(cmd.r))
        elif cmd.op=='==':
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)==self.resolve_val(cmd.r))
        elif cmd.op=='<<':
            if self.resolve_val(cmd.l).bit_length()+self.resolve_val(cmd.r)>100000:
                raise OverflowError
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)<<self.resolve_val(cmd.r))
        elif cmd.op=='>>':
            self.vars[cmd.target_var]=int(self.resolve_val(cmd.l)>>self.resolve_val(cmd.r))
        elif cmd.op=='=':
            self.vars[cmd.target_var]=self.resolve_val(cmd.l)

def parse_command(cmdstr):
    cmdstr=re.sub("\s","",cmdstr)
    m=re.match("^([A-Z])=([A-Z]|-?\d+)$",cmdstr)
    if m:
        return Command(m[1],"=",m[2])
    m=re.match("^([A-Z])=([A-Z]|-?\d+)([+\-*/%&|^><]|[><!=]=|<<|>>)([A-Z]|-?\d+)$",cmdstr)
    if m:
        return Command(m[1],m[3],m[2],m[4])
    m=re.match("^([A-Z])=-([A-Z])$",cmdstr)
    if m:
        return Command(m[1],"-",0,m[2])
    raise SyntaxError

def run_commands(fun, init_state):
    comp=Computation()
    comp.vars.update(init_state)
    try:
        for i in fun:
            comp.run(i)
    except Exception as e:
        pass # exceptions are suppressed
    return comp.vars

def input_function(line_limit, cmd_limit):
    fun=[]
    while True:
        line = input().strip()
        if line == "EOF":
            break
        if len(line)>line_limit:
            assert False, "command too long"
        fun.append(parse_command(line))
        if len(fun)>cmd_limit:
            assert False, "too many commands"
    return fun

flag=open(f"flag.txt").read().strip()
assert len(flag)<32

print("Enter your function A:")
fun_A=input_function(100,30)


flag_array=list(flag.encode()) # the flag is static
A=[]
B=[]
for i in range(100):
    cur_A=bytes_to_long(bytes(flag_array))
    cur_res=run_commands(fun_A,{"A":cur_A})
    A.append(cur_A)
    B.append(cur_res["B"])
    random.shuffle(flag_array)

assert len(set(B))==1, "results are not same"

target_B=bytes_to_long(bytes(sorted(flag_array)))
if target_B==B[0]:
    print(flag)
else:
    print("You did not sort correctly")
exit(0)
