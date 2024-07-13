from Crypto.Util.number import *
from random import *

flag = b'REDACTED'

p = 96517490730367252566551196176049957092195411726055764912412605750547823858339
a = 1337

flag = bin(bytes_to_long(flag))[2:]
encrypt = []

for bit in flag:
    encrypt.append(pow(a, (randint(2, p) * randrange(2, p, 2)) + int(bit), p))
    
print(encrypt)
