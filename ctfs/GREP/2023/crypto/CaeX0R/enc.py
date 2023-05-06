#enc.py
from random import *
flag="REDACTED"
a=randint(1,1000)
c=[]
for f in flag:
   c.append(str(ord(f)^a))
print(c)
print(a)

#c=['162', '177', '188', '169', '136', '187', '138', '145', '172', '187', '138', '145', '172', '190', '152', '156', '187', '195', '177', '142']
#a=REDACTED