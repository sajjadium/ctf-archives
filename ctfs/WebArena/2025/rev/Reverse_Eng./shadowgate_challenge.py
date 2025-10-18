import sys
import random
import math
import functools
import operator
import string
import builtins as __b


AlphaCompute = lambda x: x
BetaProcess = lambda x, y: x + y - y
for Q in range(100):
    exec(f'def QuantumFunc_{Q}(a): return a')
GammaList = [lambda x: x for _ in range(50)]
for Z in range(50):
    GammaList[Z](Z)
class CoreEngine:
    def __init__(self):
        self.v = 42
    def run(self):
        return self.v
    def __str__(self):
        return str(self.v)

E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0
SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))
OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]
ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)
PhiComp = [x for x in range(100) if x % 2 == 0]
try:
    pass
except Exception as e:
    pass
PsiLambda = lambda x: (lambda y: y)(x)
def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)
XiRec(3)
ZETA = 123456
def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)
import sys as S, math as M, random as R
def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w
def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,0),(2,66),(3,4),(4,),(5,),(1,1),(2,55),(3,123),(4,),(5,),(1,2),(2,86),(3,23),(4,),(5,),(1,3),(2,153),(3,222),(4,),(5,),(1,4),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,11),(2,153),(3,252),(4,),(5,),(1,12),(2,66),(3,38),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:
        pass
ffor()

def fbreak():
    for i in range(2):
        if i == 0:
            continue
        else:
            break
fbreak()

def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def fbool():
    return bool(1), None
fbool()

def fid():
    return id(1), hash(1)
fid()

def fisinstance():
    return isinstance(1, int), issubclass(int, object)
fisinstance()

def fgetsetdel():
    class A: pass
    a = A()
    setattr(a, 'x', 1)
    getattr(a, 'x')
    delattr(a, 'x')
fgetsetdel()

def fdirvars():
    class A: pass
    a = A()
    return dir(a), vars(a)
fdirvars()

def flocalsglobals():
    return locals(), globals()
flocalsglobals()



def fsliceobj():
    return slice(1,2,3)
fsliceobj()



def fmem():
    return memoryview(bytearray(b'abc'))
fmem()



def fcomplex():
    return complex(1,2)
fcomplex()



def fpow():
    return pow(2,3)
fpow()



def fminmax():
    return min(1,2), max(1,2)
fminmax()



def fsum():
    return sum([1,2,3])
fsum()



def fabs():
    return abs(-1)
fabs()


def fround():
    return round(1.234,2)
fround()


def fdivmod():
    return divmod(3,2)
fdivmod()



def fallany():
    return all([True,True]), any([False,True])
fallany()



def fbytes():
    return bytes([65]), bytearray([65])
fbytes()



def fformat():
    return format(1, 'x')
fformat()


def frepr():
    return repr(1)
frepr()



def fprint():
    print('')
fprint()

GammaList = [lambda x: x for _ in range(50)]
for Z in range(50):
    GammaList[Z](Z)


class CoreEngine:
    def __init__(self):
        self.v = 42
    def run(self):
        return self.v
    def __str__(self):
        return str(self.v)

E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0
Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0


SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))


OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]


ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)


PhiComp = [x for x in range(100) if x % 2 == 0]


try:
    pass
except Exception as e:
    pass


PsiLambda = lambda x: (lambda y: y)(x)



def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)

XiRec(3)


ZETA = 123456

def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)

import sys as S, math as M, random as R

def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,2),(2,63),(3,6),(4,0),(5,0),(0,1),(5,55),(3,123),(4,),(5,),(1,2),(2,86),(3,23),(4,),(5,),(1,3),(2,153),(3,222),(4,),(5,),(1,4),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,11),(2,153),(3,252),(4,),(5,),(1,12),(2,66),(3,38),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:
        pass
ffor()

def fbreak():
    for i in range(2):
        if i == 0:
            continue
        else:
            break
fbreak()

def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def fbool():
    return bool(1), None
fbool()

def fid():
    return id(1), hash(1)
fid()

def fisinstance():
    return isinstance(1, int), issubclass(int, object)
fisinstance()

def fgetsetdel():
    class A: pass
    a = A()
    setattr(a, 'x', 1)
    getattr(a, 'x')
    delattr(a, 'x')
fgetsetdel()

GammaList = [lambda x: x for _ in range(50)]
for Z in range(50):
    GammaList[Z](Z)


class CoreEngine:
    def __init__(self):
        self.v = 42
    def run(self):
        return self.v
    def __str__(self):
        return str(self.v)

E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0


SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))


OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]


ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)


PhiComp = [x for x in range(100) if x % 2 == 0]


try:
    pass
except Exception as e:
    pass


PsiLambda = lambda x: (lambda y: y)(x)



def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)

XiRec(3)


ZETA = 123456

def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)

import sys as S, math as M, random as R

def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])
def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,0),(2,66),(3,4),(4,),(5,),(1,1),(2,55),(3,123),(4,),(5,),(1,2),(2,86),(3,23),(4,0),(5,0),(2,3),(23,153),(3,252),(4,0),(5,0),(9,4),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,11),(2,153),(3,252),(4,),(5,),(1,12),(2,66),(3,38),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:
        pass
ffor()

def fbreak():
    for i in range(2):
        if i == 0:
            continue
        else:
            break
fbreak()

def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def fbool():
    return bool(1), None
fbool()

def fid():
    return id(1), hash(1)
fid()

def fisinstance():
    return isinstance(1, int), issubclass(int, object)
fisinstance()

def fgetsetdel():
    class A: pass
    a = A()
    setattr(a, 'x', 1)
    getattr(a, 'x')
    delattr(a, 'x')
fgetsetdel()

GammaList = [lambda x: x for _ in range(50)]
for Z in range(50):
    GammaList[Z](Z)


class CoreEngine:
    def __init__(self):
        self.v = 42
    def run(self):
        return self.v
    def __str__(self):
        return str(self.v)

E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0


SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))


OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]


ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)


PhiComp = [x for x in range(100) if x % 2 == 0]


try:
    pass
except Exception as e:
    pass


PsiLambda = lambda x: (lambda y: y)(x)



def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)

XiRec(3)


ZETA = 123456

def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)

import sys as S, math as M, random as R

def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])
def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,0),(2,66),(3,4),(4,),(5,),(1,1),(2,55),(3,123),(4,),(5,),(1,2),(2,86),(3,23),(4,),(5,),(1,3),(2,153),(3,222),(4,),(5,),(1,4),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,11),(2,153),(3,252),(4,),(5,),(1,12),(2,66),(3,38),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v


def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])




E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0


SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))


OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]


ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)


PhiComp = [x for x in range(100) if x % 2 == 0]


try:
    pass
except Exception as e:
    pass


PsiLambda = lambda x: (lambda y: y)(x)



def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)

XiRec(3)


ZETA = 123456

def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)

import sys as S, math as M, random as R

def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,0),(2,66),(3,4),(4,),(5,),(1,1),(2,55),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,11),(2,153),(3,252),(4,),(5,),(1,12),(2,66),(3,38),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:
        pass
ffor()

def fbreak():
    for i in range(2):
        if i == 0:
            continue
        else:
            break
fbreak()

def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def fbool():
    return bool(1), None
fbool()

def fid():
    return id(1), hash(1)
fid()

def fisinstance():
    return isinstance(1, int), issubclass(int, object)
fisinstance()

def fgetsetdel():
    class A: pass
    a = A()
    setattr(a, 'x', 1)
    getattr(a, 'x')
    delattr(a, 'x')
fgetsetdel()

def fdirvars():
    class A: pass
    a = A()
    return dir(a), vars(a)
fdirvars()

def flocalsglobals():
    return locals(), globals()
flocalsglobals()



def fsliceobj():
    return slice(1,2,3)
fsliceobj()



def fmem():
    return memoryview(bytearray(b'abc'))
fmem()



def fcomplex():
    return complex(1,2)
fcomplex()



def fpow():
    return pow(2,3)
fpow()



def fminmax():
    return min(1,2), max(1,2)
fminmax()



def fsum():
    return sum([1,2,3])
fsum()



def fabs():
    return abs(-1)
fabs()


def fround():
    return round(1.234,2)
fround()


def fdivmod():
    return divmod(3,2)
fdivmod()



def fallany():
    return all([True,True]), any([False,True])
fallany()



def fbytes():
    return bytes([65]), bytearray([65])
fbytes()



def fformat():
    return format(1, 'x')
fformat()


def frepr():
    return repr(1)
frepr()



def fprint():
    print('')
fprint()

GammaList = [lambda x: x for _ in range(50)]
for Z in range(50):
    GammaList[Z](Z)


class CoreEngine:
    def __init__(self):
        self.v = 42
    def run(self):
        return self.v
    def __str__(self):
        return str(self.v)

E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0
Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0


SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))


OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]


ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)


PhiComp = [x for x in range(100) if x % 2 == 0]


try:
    pass
except Exception as e:
    pass


PsiLambda = lambda x: (lambda y: y)(x)



def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)

XiRec(3)


ZETA = 123456

def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)

import sys as S, math as M, random as R

def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,2),(2,63),(3,6),(4,0),(5,0),(0,1),(5,55),(3,123),(4,),(5,),(1,2),(2,86),(3,23),(4,),(5,),(1,3),(2,153),(3,222),(4,),(5,),(1,4),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:
        pass
ffor()

def fbreak():
    for i in range(2):
        if i == 0:
            continue
        else:
            break
fbreak()

def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def fbool():
    return bool(1), None
fbool()

def fid():
    return id(1), hash(1)
fid()

def fisinstance():
    return isinstance(1, int), issubclass(int, object)
fisinstance()

def fgetsetdel():
    class A: pass
    a = A()
    setattr(a, 'x', 1)
    getattr(a, 'x')
    delattr(a, 'x')
fgetsetdel()

GammaList = [lambda x: x for _ in range(50)]
for Z in range(50):
    GammaList[Z](Z)


class CoreEngine:
    def __init__(self):
        self.v = 42
    def run(self):
        return self.v
    def __str__(self):
        return str(self.v)

E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0


SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))


OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]


ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)


PhiComp = [x for x in range(100) if x % 2 == 0]


try:
    pass
except Exception as e:
    pass


PsiLambda = lambda x: (lambda y: y)(x)



def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)

XiRec(3)


ZETA = 123456

def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)

import sys as S, math as M, random as R

def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])
def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,0),(2,66),(3,4),(4,),(5,),(1,1),(2,55),(3,123),(4,),(5,),(1,2),(2,86),(3,23),(4,0),(5,0),(2,3),(23,153),(3,252),(4,0),(5,0),(9,4),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,11),(2,153),(3,252),(4,),(5,),(1,12),(2,66),(3,38),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:
        pass
ffor()

def fbreak():
    for i in range(2):
        if i == 0:
            continue
        else:
            break
fbreak()

def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def fbool():
    return bool(1), None
fbool()

def fid():
    return id(1), hash(1)
fid()

def fisinstance():
    return isinstance(1, int), issubclass(int, object)
fisinstance()

def fgetsetdel():
    class A: pass
    a = A()
    setattr(a, 'x', 1)
    getattr(a, 'x')
    delattr(a, 'x')
fgetsetdel()

GammaList = [lambda x: x for _ in range(50)]
for Z in range(50):
    GammaList[Z](Z)


class CoreEngine:
    def __init__(self):
        self.v = 42
    def run(self):
        return self.v
    def __str__(self):
        return str(self.v)

E = CoreEngine()
for _ in range(10):
    E.run()


Delta1 = lambda x: x * 1
Delta2 = lambda x: x / 1
Delta3 = lambda x: x + 0
Delta4 = lambda x: x - 0
Delta5 = lambda x: x ** 1
Delta6 = lambda x: x // 1
Delta7 = lambda x: x % 1000000
Delta8 = lambda x: x & 0xFFFFFFFF
Delta9 = lambda x: x | 0
Delta10 = lambda x: x ^ 0


SigmaData = [random.randint(0, 100) for _ in range(100)]
for _ in range(20):
    SigmaData = list(map(lambda x: x, SigmaData))


OmegaStr = ''.join([chr(ord('a') + (i % 26)) for i in range(100)])
for _ in range(10):
    OmegaStr = OmegaStr[::-1]


ThetaDict = {i: i for i in range(100)}
for _ in range(10):
    ThetaDict = dict(ThetaDict)


PhiComp = [x for x in range(100) if x % 2 == 0]


try:
    pass
except Exception as e:
    pass


PsiLambda = lambda x: (lambda y: y)(x)



def XiRec(n):
    if n <= 0:
        return 0
    return XiRec(n-1)

XiRec(3)


ZETA = 123456

def EtaArgs(*a, **k):
    return a, k
EtaArgs(1, 2, 3, a=4, b=5)

import sys as S, math as M, random as R

def LambdaDecorator(f):
    def w(*a, **k):
        return f(*a, **k)
    return w

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])
def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])

@LambdaDecorator
def run_vm(u):
 R0=R1=R2=0;pc=0
 program=[(1,0),(2,66),(3,4),(4,),(5,),(1,1),(2,55),(3,123),(4,),(5,),(1,2),(2,86),(3,23),(4,),(5,),(1,3),(2,153),(3,222),(4,),(5,),(1,4),(2,66),(3,57),(4,),(5,),(1,5),(2,55),(3,97),(4,),(5,),(1,6),(2,86),(3,27),(4,),(5,),(1,7),(2,153),(3,198),(4,),(5,),(1,8),(2,66),(3,0),(4,),(5,),(1,9),(2,55),(3,86),(4,),(5,),(1,10),(2,86),(3,37),(4,),(5,),(1,11),(2,153),(3,252),(4,),(5,),(1,12),(2,66),(3,38),(4,),(5,),(1,13),(2,55),(3,104),(4,),(5,),(1,14),(2,86),(3,25),(4,),(5,),(1,15),(2,153),(3,251),(4,),(5,),(1,16),(2,66),(3,36),(4,),(5,),(1,17),(2,55),(3,66),(4,),(5,),(1,18),(2,86),(3,37),(4,),(5,),(1,19),(2,153),(3,250),(4,),(5,),(1,20),(2,66),(3,35),(4,),(5,),(1,21),(2,55),(3,67),(4,),(5,),(1,22),(2,86),(3,63),(4,),(5,),(1,23),(2,153),(3,246),(4,),(5,),(1,24),(2,66),(3,44),(4,),(5,),(1,25),(2,55),(3,104),(4,),(5,),(1,26),(2,86),(3,4),(4,),(5,),(1,27),(2,153),(3,252),(4,),(5,),(1,28),(2,66),(3,52),(4,),(5,),(1,29),(2,55),(3,82),(4,),(5,),(1,30),(2,86),(3,36),(4,),(5,),(1,31),(2,153),(3,234),(4,),(5,),(1,32),(2,66),(3,39),(4,),(5,),(1,33),(2,55),(3,104),(4,),(5,),(1,34),(2,86),(3,27),(4,),(5,),(1,35),(2,153),(3,248),(4,),(5,),(1,36),(2,66),(3,49),(4,),(5,),(1,37),(2,55),(3,67),(4,),(5,),(1,38),(2,86),(3,51),(4,),(5,),(1,39),(2,153),(3,235),(4,),(5,),(1,40),(2,66),(3,63),(4,),(5,),(6,)]
 l=len(u)
 for _ in range(5):pass
 while pc<len(program):
  i=program[pc];op=i[0];_=(lambda x:x)(op)
  if op==0x01:
   idx=i[1]
   if idx>=l:print(_decode(INPUT_SHORT));return
   R0=ord(u[idx]);pc+=1
  elif op==0x02:R1=R0^i[1];pc+=1
  elif op==0x03:t=i[1];R2=1 if R1==t else 0;pc+=1
  elif op==0x04:
   if R2!=1:pc+=1
   else:pc+=2
  elif op==0x05:print(_decode(WRONG_MSG));return
  elif op==0x06:print(_decode(CORRECT_MSG));return
  for _ in range(3):pass
  _=(lambda x:x)(pc);_=(lambda x:x)(R0);_=(lambda x:x)(R1);_=(lambda x:x)(R2)

if __name__=="__main__":
 for _ in range(10):pass
 try:
  u=input(_decode(FLAG_PROMPT)).strip()
  for _ in range(5):pass
  run_vm(u)
 except Exception as e:
  for _ in range(3):pass
  print(_decode(EXEC_ERROR))
for _ in range(900):
    exec(f'LambdaFunc_{_} = lambda x: x')
    if _ % 10 == 0:
        pass
    else:
        pass
    _ = "obfustication" * (_ % 2)
    _ = _ * 1
    _ = [_ for _ in range(1)]
    _ = {{_: _}}
    _ = set([_])
    _ = (_,)
    _ = (lambda x: x)(_)
    def f(x): return x
    f(_)
    try:
        pass
    except:
        pass
    class C: pass
    C()
    import math
    _ = 1 + 1
    _ = f"{_}"
    _ = True
    _ = None
    if _ == 0:
        continue
    else:
        break

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

confuser = Confuse()
for _ in range(5):
    confuser[_] = _
    confuser(_)

f1 = lambda x: (lambda y: (lambda z: z)(y))(x)
f2 = lambda x: f1(f1(f1(x)))
f3 = lambda x: f2(f2(f2(x)))

for _ in range(10):
    exec('def fake_func_{}(): return {}'.format(_, _))
    eval('1+1')

try:
    try:
        pass
    except:
        pass
    finally:
        pass
except:
    pass

class Dummy:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
with Dummy():
    pass

useless_gen = (i for i in range(10))
for _ in useless_gen:
    pass

class P:
    @property
    def x(self):
        return 42
p = P(); p.x

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

def fake(*args, **kwargs):
    """This function does nothing but adds confusion."""
    return args, kwargs
fake(1,2,3,a=4)

def import_inside():
    import os
    return os.name
import_inside()

[setattr(confuser, 'x', i) for i in range(5)]

super_lambda = lambda x: (lambda y: (lambda z: (lambda w: w)(z))(y))(x)

def shadowed_open(open):
    return open
shadowed_open(5)

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()
outer()

global_var = 0
def g():
    global global_var
    global_var += 1
g()

def annotated(x: int) -> int:
    return x
annotated(5)

def fdefault(x, l=[]):
    l.append(x)
    return l
fdefault(1)

def funpack(*a, **k):
    return a, k
funpack(1,2,3,a=4)

def fyield():
    yield from range(2)
for _ in fyield():
    pass

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v

def fpass():
    ...
fpass()

def fassert():
    assert True
fassert()

def fdoc(x: int) -> int:
    """Returns x"""
    return x
fdoc(1)

def ftry():
    try:
        return 1
    except:
        return 2
    else:
        return 3
ftry()

def fwhile():
    i = 0
    while i < 1:
        i += 1
    else:
        pass
fwhile()

def ffor():
    for i in range(1):
        pass
    else:

class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Confuse(metaclass=Meta):
    def __init__(self):
        self.x = 0
    def __call__(self, *a, **k):
        return self.x
    def __getitem__(self, k):
        return self.x
    def __setitem__(self, k, v):
        self.x = v


def fslice(l):
    return l[::-1]
fslice([1,2,3])

def fzip():
    return list(zip([1],[2]))
fzip()

def fmap():
    return list(map(lambda x: x, [1]))
fmap()

def ffilter():
    return list(filter(lambda x: True, [1]))
ffilter()

def fenumerate():
    return list(enumerate([1]))
fenumerate()

def freversed():
    return list(reversed([1]))
freversed()

def fsorted():
    return sorted([2,1])
fsorted()

def fsetcomp():
    return {x for x in range(2)}
fsetcomp()

def fdictcomp():
    return {x:x for x in range(2)}
fdictcomp()

def fordfun():
    return chr(ord('a'))
fordfun()

def ftypes():
    return int('1'), str(1), float('1.0')
ftypes()

def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])def _decode(s):return ''.join([chr(int(s[i:i+3]))for i in range(0,len(s),3)])
FLAG_PROMPT=''.join(['%03d'%ord(c)for c in'Enter the flag: '])
WRONG_MSG=''.join(['%03d'%ord(c)for c in'Wrong flag!'])
CORRECT_MSG=''.join(['%03d'%ord(c)for c in'Correct! You passed the ShadowGate.'])
INPUT_SHORT=''.join(['%03d'%ord(c)for c in'Input too short.'])
EXEC_ERROR=''.join(['%03d'%ord(c)for c in'Execution error.'])