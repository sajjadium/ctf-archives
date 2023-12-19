from Crypto.Util.number import getPrime, bytes_to_long
from secret import FLAG

m = bytes_to_long(FLAG)
f = open ('output.txt', 'w')
e = 37
n = [getPrime(1024)*getPrime(1024) for i in range(e)]
c = [pow(m, e, n[i]) for i in range(e)]

with open ('output.py', 'w'):
    f.write(f"e = {e}\n")
    f.write(f"c = {c}\n")
    f.write(f"n = {n}\n")

