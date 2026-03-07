from Crypto.Util.number import *
from Crypto.Hash import SHA256
import secrets

def hsh(x):
  h = SHA256.new()
  h.update(x)
  return int.from_bytes(h.digest())
  

for i in range(10):
  S=set()
  p=getPrime(70)
  print(f"{p=}")
  x=secrets.randbelow(p)
  while True:
    m1=input("m1=")
    if "Stop" in m1:
      break
    m1=bytes.fromhex(m1)
    if m1 in S:
      print("NO!")
      exit(0)
    S.add(m1)
    m2=bytes.fromhex(input("m2="))
    if m2 in S:
      print("NO!")
      exit(0)
    S.add(m2)
    
    res=pow(x,hsh(m1),p)+pow(x,hsh(m2),p)
    res%=p
    print(f"{res=}")
  
  x2=int(input("x="))
  if x2!=x:
    print("FAIL!")
    exit(0)

print(open("flag.txt","r").read())
    
