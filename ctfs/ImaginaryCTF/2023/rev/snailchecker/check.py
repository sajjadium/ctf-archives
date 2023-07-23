#!/usr/bin/env python3

def enc(b):
 a = [n for n in range(b[0]*2**24+b[1]*2**16+b[2]*2**8+b[3]+1)][1:]
 c,i = 0,0
 while len([n for n in a if n != 0]) > 1:
  i%=len(a)
  if (a[i]!=0 and c==1):
   a[i],c=0,0
  if (a[i] != 0):
   c+=1
  i += 1
 return sum(a)

print(r"""
    .----.   @   @
   / .-"-.`.  \v/
   | | '\ \ \_/ )
 ,-\ `-.' /.'  /
'---`----'----'
""")
flag = input("Enter flag here: ").encode()
out = b''
for n in [flag[i:i+4] for i in range(0,len(flag),4)]:
  out += bytes.fromhex(hex(enc(n[::-1]))[2:].zfill(8))

if out == b'L\xe8\xc6\xd2f\xde\xd4\xf6j\xd0\xe0\xcad\xe0\xbe\xe6J\xd8\xc4\xde`\xe6\xbe\xda>\xc8\xca\xca^\xde\xde\xc4^\xde\xde\xdez\xe8\xe6\xde':
 print("[*] Flag correct!")
else:
 print("[*] Flag incorrect.")
