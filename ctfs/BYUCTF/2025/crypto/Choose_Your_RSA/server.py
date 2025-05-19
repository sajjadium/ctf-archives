#!/usr/local/bin/python

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime
from Crypto.Util.Padding import pad
import os


print("[+] Generating values...", flush=True)
flag = open("/app/flag.txt").read().encode()
key = os.urandom(160)
p, q, n, e = [], [], [], []
for i in range(3):
    p.append(getPrime(1024+512*i))
    q.append(getPrime(1024+512*i))
    n.append(p[i]*q[i])


cipher = AES.new(key[:16], AES.MODE_ECB)
print(cipher.encrypt(pad(flag, AES.block_size)).hex())
print("We will encrypt the key three times, and you can even choose the value of e. Please put your distinct e values in increasing order.")

try:
    e = list(map(int, input().split(" ")))
    assert e[0]>1
    assert e[1]>e[0]
    assert e[2]>e[1]
except Exception as e:
    print("sorry, invalid input")
    quit()

key = bytes_to_long(key)
for i in range(3):
    print(f"n{i}=",n[i], sep="")
    print(f"c{i}=", pow(key, e[i], n[i]), sep="")