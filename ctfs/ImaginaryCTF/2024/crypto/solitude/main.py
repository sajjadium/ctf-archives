#!/usr/bin/env python3

import random

def xor(a: bytes, b: bytes):
  out = []
  for m,n in zip(a,b):
    out.append(m^n)
  return bytes(out)

class RNG():
  def __init__(self, size, state=None):
    self.size = size
    self.state = list(range(self.size+2))
    random.shuffle(self.state)
  def next(self):
    idx = self.state.index(self.size)
    self.state.pop(idx)
    self.state.insert((idx+1) % (len(self.state)+1), self.size)
    if self.state[0] == self.size:
      self.state.pop(0)
      self.state.insert(1, self.size)
    idx = self.state.index(self.size+1)
    self.state.pop(idx)
    self.state.insert((idx+1) % (len(self.state)+1), self.size+1)
    if self.state[0] == self.size+1:
      self.state.pop(0)
      self.state.insert(1, self.size+1)
    if self.state[1] == self.size+1:
      self.state.pop(1)
      self.state.insert(2, self.size+1)
    c1 = self.state.index(self.size)
    c2 = self.state.index(self.size+1)
    self.state = self.state[max(c1,c2)+1:] + [self.size if c1<c2 else self.size+1] + self.state[min(c1,c2)+1:max(c1,c2)] + [self.size if c1>c2 else self.size+1] + self.state[:min(c1,c2)]
    count = self.state[-1]
    if count in [self.size,self.size+1]:
      count = self.size
    self.state = self.state[count:-1] + self.state[:count] + self.state[-1:]
    idx = self.state[0]
    if idx in [self.size,self.size+1]:
      idx = self.size
    out = self.state[idx]
    if out in [self.size,self.size+1]:
      out = self.next()
    return out

if __name__ == "__main__":
  flag = open("flag.txt", "rb").read()
  while True:
    i = int(input("got flag? "))
    for _ in range(i):
      rng = RNG(128)
      stream = bytes([rng.next() for _ in range(len(flag))])
      print(xor(flag, stream).hex())
