import os
from Crypto.Util.number import *
from hashlib import *
from binascii import unhexlify

LEN = 17
magic = os.urandom(LEN)
print("Magic:", magic.hex())
print('Coud you use it to solve dlog?')

magic_num = bytes_to_long(magic)
try:
    P = int(input('P:>'))
    e = int(input('E:>'))
    data = unhexlify(input('data:>'))
    if P >> (384 - LEN*8) == magic_num and isPrime(P):
        data2 = sha384(data).digest()
        num1 = bytes_to_long(data)
        num2 = bytes_to_long(data2)
        if pow(num1, e, P) == num2:
            print(open('flag','r').read())
        else:
            print('try harder!!!')
    else:
        print('try harder!')
except Exception as e:
    print('invalid')
