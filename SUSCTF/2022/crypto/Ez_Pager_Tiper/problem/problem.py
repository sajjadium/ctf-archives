from Crypto.Util.number import *
from magic_box import *
from secret import mask1, mask2, seed1, seed2, seed3
n1, n2 = 64, 12

flag = 'SUSCTF{***}'

def encrypt(cipher, ipath, opath):
    ifile=open(ipath,'rb')
    ofile=open(opath,'wb')
    plaintext=ifile.read()
    for ch in plaintext:
        c=ch^cipher.getrandbit(8)
        ofile.write(long_to_bytes(c))
    ifile.close()
    ofile.close()

def problem1():
    r = getRandomInteger(6)
    magic = 1<<r
    lfsr1 = lfsr(seed1, mask1, n1)
    lfsr2 = lfsr(seed2, mask2, n2)
    cipher = generator(lfsr1, lfsr2, magic)
    encrypt(cipher, "MTk4NC0wNC0wMQ==_6d30.txt", "MTk4NC0wNC0wMQ==_6d30.enc")

def problem2():
    magic = getPrime(64)
    lfsr1=lfsr(seed1, mask1, n1)
    lfsr2=lfsr(seed3, mask2, n2)
    cipher = generator(lfsr1, lfsr2, magic)
    encrypt(cipher, "MTk4NC0xMi0yNQ==_76ff.txt", "MTk4NC0xMi0yNQ==_76ff.enc")
    # flag in it?
    print(f'hint={magic}')
    # hint = 15193544052573546419

problem1()
problem2()
