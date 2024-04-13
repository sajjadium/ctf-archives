import math
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import os

num_bits = 4096
e = (num_bits - 1) * 2
n = getPrime(num_bits)

with open("flag.txt","rb") as f:
    flag = f.read()

m = bytes_to_long(flag)
c = pow(m, e, n)
print(c)

with open("output.txt", "w") as f:
	f.write("e = {0}\n".format(e))
	f.write("n = {0}\n".format(n))
	f.write("c = {0}\n".format(c))

