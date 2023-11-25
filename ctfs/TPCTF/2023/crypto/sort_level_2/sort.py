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

level=int(input("Level: "))
assert level in [1,2]

flag=open(f"flag{level}.txt").read().strip()
assert len(flag)<32

print("Enter your function A:")
if level==1:
    fun_A=input_function(100,1000)
else:
    fun_A=input_function(10,500)
    print("Enter your function B:")
    fun_B=input_function(10,500)

# first try some fake flags
B=[]
for i in range(5):
    cur_res=run_commands(fun_A,{"A":bytes_to_long(b'TPCTF{'+bytes([random.randint(49,122) for i in range(24)])+b'}')})
    B.append(cur_res["B"])

for i in range(5):
    cur_res=run_commands(fun_A,{"A":bytes_to_long(bytes([random.randint(49,122) for i in range(24)]))})
    B.append(cur_res["B"])

assert len(set(B))==10, "don't cheat"

flag_array=list(flag.encode()) # the flag is static
A=[]
B=[]
C=[]
for i in range(100):
    cur_A=bytes_to_long(bytes(flag_array))
    cur_res=run_commands(fun_A,{"A":cur_A})
    A.append(cur_A)
    B.append(cur_res["B"])
    C.append(cur_res["C"])
    if i<=10:
        flag_array_inner=flag_array[6:-1]
        random.shuffle(flag_array_inner)
        flag_array[6:-1]=flag_array_inner
    else:
        random.shuffle(flag_array)


if level==1:
    target_B=bytes_to_long(bytes(sorted(flag_array)))
    if [target_B]==list(set(B)):
        print(flag)
    else:
        print("You did not sort correctly")
    exit(0)

assert len(set(B))==1, "results are not same"

assert max(C).bit_length()<=120, "result too long"
for i in range(100):
    assert A[i]==run_commands(fun_B,{"B":B[i],"C":C[i]})["A"]

C0=str(C[0])
print("Here is your gift:")
print("B =",B[0])
print("C =",C0[:3]+'*'*(len(C0)-3))
    