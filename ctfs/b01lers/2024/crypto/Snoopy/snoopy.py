import time
import os
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random.random import randrange
from numba import jit


FLAG = open("flag.txt", "rb").read().strip()
assert FLAG[:5] == b"bctf{" and FLAG[-1:] == b"}"
FLAG = FLAG[5:-1]
assert len(FLAG) <= 16

HI = 3.3


@jit(nopython = True)   # serious python computations need something like this..
def sweep(m, turbo = 0.):
  res = m.copy()
  nx,ny = res.shape
  eps = 0.
  for i in range(1, nx - 1):
    for j in range(1, ny - 1):
      d = 0.25 * (m[i, j+1] + m[i, j-1] + m[i+1, j] + m[i-1, j]) - m[i,j]
      res[i,j] += d * (1. - turbo)
      eps = max(eps, abs(d)) 
  return res, eps


class Snoopy:
  def __init__(self, N):
    self.N = N
    self.die = np.zeros((N + 1, N + 1), dtype = float)
    self.on = False

  def mapPin(self, k):
    N = self.N
    if k < N:      return 0,        k
    elif k < 2*N:  return k % N,    N
    elif k < 3*N:  return N,        (-k) % N
    else:          return (-k) % N, 0

  def setPin(self, k, v):
    i,j = self.mapPin(k)
    self.die[i,j] = v

  def getPin(self, k):
    i,j = self.mapPin(k)
    return self.die[i,j]

  # solely keeping this for backwards compatibility (original tech limitations are long gone)
  def firstPin(self, idx):
    N4 = self.N >> 2
    return ((idx % N4) << 4) + (0   if idx < N4   else   8)

  def load(self, idx):
    first = self.firstPin(idx % (self.N >> 1))
    return sum( [ (1 << k)   for k in range(8)   if self.getPin(first + k) == HI ] )

  def save(self, idx, v):
    first = self.firstPin(idx % (self.N >> 1))
    for k in range(8):   self.setPin(first + k, HI * ((v >> k) & 1))

  def swap(self, idx1, idx2):
    v1 = self.load(idx1)
    v2 = self.load(idx2)
    self.save(idx1, v2)
    self.save(idx2, v1)
    
  def inc(self, idx):
    v = self.load(idx)
    self.save(idx, v + 1)

  def boot(self):
    r = b"SnOoPy@BCtf2024#"
    for idx in range(self.N >> 1):
      self.save(idx, r[idx % len(r)])
      time.sleep(0.1)
    self.save(-1, 0)
    self.on = True

  def placeLoop(self):
    if self.on:
      print("** Tampering detected **\nShutting down", flush = True)
      exit(0)
    GAP = 10
    while True:
      try:
        x0,y0 = [int(v)   for v in input("top left corner: ").strip().split() ]
        x1,y1 = [int(v)   for v in input("bottom right corner: ").strip().split() ]
        if GAP < x0 < x1 < self.N - GAP and GAP < y0 < y1 < self.N - GAP:
          self.loop = ((x0,y0), (x1,y1))
          break
      except ValueError:  pass

  def keygen(self):
    self.swap(-1, 1)
    for k in range(self.N >> 3):  self.save(-k, os.urandom(1)[0])
    self.swap(-1, 1)
    self.inc(-1)
    if self.load(-1) == 0:
      print("** Ran out of keys **\nShutting down", flush = True)
      exit(0)

  def encrypt(self):
    N = self.N
    for i in range(1, N):
      for j in range(1, N):
        self.die[i, j] = HI * randrange(0, 2**64) / 2**64
    self.keygen()
    x = bytes( [ self.load(-k)   for k in range(N >> 3) ] )
    aes = AES.new(x*4, AES.MODE_ECB)
    c = aes.encrypt(FLAG)
    for k in range(len(c)):  self.save(k, c[k])
    return self.magic()

  def magic(self):
    for _ in range(200000):
      #self.die, eps = sweep(self.die, 0.)
      self.die, eps = sweep(self.die, 0.01)   # save some on datacenter costs (US Patent No. 20240412)
      if eps < 1e-14:  return True
    return False

  def snoop(self):
    ((i1, j1), (i2,j2)) = self.loop 
    # cheapo gear constraints (this is a shoestring op :/)
    if min(i2 - i1, j2 - j1) < 10: 
      print("** Short circuit in detector **", flush = True)
      exit(0)      
    if (i2 - i1) + (j2 - j1) > 40:
      print("** Tampering detected **\nShutting down", flush = True)
      exit(0)      
    data =  [ self.die[i1, j]  for j in range(j1, j2) ]
    data += [ self.die[i, j2]  for i in range(i1, i2) ]
    data += [ self.die[i2, j]  for j in range(j2, j1, -1) ]
    data += [ self.die[i, j1]  for i in range(i2, i1, -1) ]
    return data

  def menu(self):
    print(
"""
Choose:
  1) place detector
  2) boot
  3) generate key
  4) encrypt flag
  5) snoop
  6) exit
""", flush = True)

  def run(self):
    self.menu()
    choice = input("> ").strip()

    if choice == "1":
      self.placeLoop()
      print(f"\nSnoop loop in place at {self.loop} :)", flush = True)

    elif choice == "2":
      print("Booting system... ", end = "", flush = True)
      self.boot()
      print("DONE", flush = True)

    elif choice == "3":
      if not self.on:  return        
      print("\nGenerating key... ", end = "", flush = True)
      self.keygen()
      print("SUCCESS", flush = True)

    elif choice == "4":
      if not self.on:  return        
      print("\nEncrypting flag... ", end = "", flush = True)
      if self.encrypt():  print("SUCCESS", flush = True)
      else:               print("FAILURE - try again", flush = True)
 
    elif choice == "5":
      if not self.on:  return
      print("\nCollecting... ", end = "", flush = True)
      try: 
        data = self.snoop()
        print("DONE", flush = True)
        print(f"Readings: {data}", flush = True) 
      except AttributeError:
        print("FAILURE", flush = True)

    elif choice == "6":  exit(0)


if __name__ == "__main__":

  chal = Snoopy(64)
  while True:  chal.run()
  
