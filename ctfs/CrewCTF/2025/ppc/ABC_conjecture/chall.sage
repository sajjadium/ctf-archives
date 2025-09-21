from Crypto.Util.number import *
from jury import jurysol

def score(inp,sol):
  for i in range(3):
    assert(sol[i]!=0)
  assert(sol[0]+sol[1]==sol[2])
  for i in range(3):
    assert(len(sol[i].roots())==inp[i])
  Mx=0
  for X in sol:
    Mx=max(Mx,X.degree())
  return Mx


p=getPrime(256)
print(f"{p=}")
F=GF(p)
R=F['x']
x=R.gen()


for a in range(0,10):
  for b in range(0,10):
    for c in range(0,10):
      print(f"Give me your solution for {a}, {b}, {c}")
      A=list(map(int,input().split(",")))
      B=list(map(int,input().split(",")))
      C=list(map(int,input().split(",")))
      A=R(A)
      B=R(B)
      C=R(C)
      Sc=score((a,b,c),(A,B,C))
      Sol=jurysol((a,b,c),p,R,x)
      Sc2=score((a,b,c),Sol)
      if Sc==Sc2:
        print("Good! Onto the next level")
        continue
      if Sc>Sc2:
        print("Your solution is not optimal")
        exit(0)
      if Sc<Sc2:
        print("Something weird happened, contact the jury")
        continue

F=open('flag.txt','rb').read()

print("You passed all levels, now you get the flag!")
print(F)
