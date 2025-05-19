from Crypto.Util.number import bytes_to_long, getPrime
import random

flag = open("flag.txt").read().encode()
flag = bytes_to_long(flag)
n = 1
while n.bit_length()<4096:
    i = random.randint(10,16)
    reps = random.randint(2,5)
    p = getPrime(i)
    if n%p !=0:
        n*=p**reps
e = 65537
encryptedFlag = pow(flag, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"flag = {encryptedFlag}")