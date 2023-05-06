import itertools
import os
import datetime
import math


FLAG = open("flag.txt", "rb").read().strip()

cache = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 
107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 
373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 
509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 
659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 
823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 
983, 991, 997]

N = 128


def makeStamp(t):  return int( "".join( str(t)[:-3].translate({45: ' ', 46: ' ', 58: ' '}).split()[::-1] ) )

def getWeights(stamp):  return sorted(cache, key = lambda v: abs(math.sin(math.pi * stamp / v)))

def f(z, key):
   A, B, p, q = key
   for _ in range(p): z = A * z * (1 - z)
   for _ in range(q): z = B * z * (1 - z)
   return z

def g(b, key):  return int(f(0.5/(N+1)*(b+1), key) * 256)

def keygen(p = None, q = None):
   A0 = 3.95
   if p == None or q == None:
      stamp = makeStamp(t0) 
      p, q = getWeights(stamp)[:2]
   while True:
      A = A0 + int.from_bytes(os.urandom(4), "big") * 1e-11
      B = A0 + int.from_bytes(os.urandom(4), "big") * 1e-11
      key = A, B, p, q
      a = sorted( [(g(b, key) << 8) + g(b^0xbc, key)  for b in range(N)] )
      s = max( [ sum([1  for _ in b]) for _,b in itertools.groupby(a)] )
      if s < 2:  return A, B, p, q

def enc(m, key):
   ctxt = [ (g(c, key) << 8) + g(c^0xbc, key)   for c in m ]
   return b"".join( [ v.to_bytes(2, "big")  for v in ctxt ])



t0 = datetime.datetime.utcnow()
credits = sum( getWeights(makeStamp(t0))[-29:] )

while True:

   if credits <= 0:
      print("out of credits :/ ")
      break

   print(
f"""
 1) encrypt message [1 credit]
 2) encrypt flag [50 credits]
 3) buy time [1000 credits]
 4) quit

You have {credits} credits.
""", flush = True
   )
   choice = input("> ")
   
   if choice == "1":
      credits -= 1
      msghex = input("message in hex: ")
      try:
         msg = bytes.fromhex(msghex)
      except ValueError:
         print("invalid hex", flush = True)
         continue
      key = keygen()
      print( enc(msg[:50], key).hex(), flush = True )


   elif choice == "2":
      credits -= 50
      key = keygen()
      print( enc(FLAG, key).hex(), flush = True )

   elif choice == "3":
      if credits < 1000:
         print("insufficient credit", flush = True)
         continue
      credits -= 1000
      try:
         delta = float( input("Time gain: ") )
         if abs(delta) > 5:  raise ValueError
         t0 += datetime.timedelta(seconds = delta)
      except ValueError:
         print("invalid input", flush = True)

   elif choice == "4": break


print("Goodbye!", flush = True)
