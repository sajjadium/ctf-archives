from Crypto.Util.number import * 
p = getPrime(1024)
bits = 100
from secret import flag
m = bytes_to_long(flag)
hints = [pow(m , -1 , p) , pow(m+1 , -2 , p)]
hints_leak = [(i>>bits)<<bits for i in hints]
print(f"hints_leak = {hints_leak}")
print(f"p = {p}")