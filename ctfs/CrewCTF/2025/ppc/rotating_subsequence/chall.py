import signal
import secrets
from check import checker

def TLE(signum, frame):
  print("Timeout!")
  exit(0)

signal.signal(signal.SIGALRM, TLE)
signal.alarm(200)

print("Let's see if you have what it takes!")

TT=50
nbits=256


for i in range(TT):
  N=secrets.randbits(nbits)
  K=secrets.randbelow(100)+3
  print(f"{N=}")
  print(f"{K=}")
  S=list(map(int,input("S=").split(",")))
  assert len(S)<=K*nbits, "Too big!"
  for i in range(len(S)):
    assert 0<=S[i] and S[i]<K, "Not in the correct range"
  assert checker(S,N,K), "Incorrect input"
  print("Good job!")
  
print("Well done! Here, take a flag for your effort:")
print(open('flag.txt','r').read())
