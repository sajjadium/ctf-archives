from Crypto.Util.number import *
p = getPrime(1024)
bits = 128
m = bytes_to_long(b"REDACTED")
hints = [pow(m , -1 , p) , pow(m+1 , -2 , p)]
hints_leak = [(i>>bits)<<bits for i in hints]
print(f'p = {p}')
print(f'hints_leak = {hints_leak}')
