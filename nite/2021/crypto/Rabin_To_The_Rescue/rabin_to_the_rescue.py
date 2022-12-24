from Crypto.Util.number import *
from sympy import *
import random

def mixer(num):
    while(num>1):
        if(int(num) & 1):
            num=3*num+1
        else:
            num=num/2
    return num

def gen_sexy_primes():
    p=getPrime(256)
    q=p+6

    while((p%4!=3)or(q%4!=3)):
        p=getPrime(256)
        q=nextprime(p+1)
    return p, q

p, q=gen_sexy_primes()
n=p*q
    

def encrypt(m, e, n):
    return pow(m, e, n)
    
e=int(mixer(q-p))*2

print("________________________________________________________________________________________________")
print("\n\n")
print("-----------------------------------")
print("-----------------------------------")
print("-----------------------------------")
print("               /\\")
print("            __/__\\__")
print("            \\/    \\/")
print("            /\\____/\\")
print("            ``\\  /``  ")
print("               \\/")
print("-----------------------------------")
print("-----------------------------------")
print("-----------------------------------")
print("\n\n")
print("Welcome to the Encryption challenge!!!!")
print("\n")
print("Menu:")
print("=> [E]ncrypt your message")
print("=> [G]et Flag")
print("=> E[x]it")
print("________________________________________________________________________________________________")

while(true):
    choice=input(">>")
    if choice.upper()=='E':
        print("Enter message in hex:")
        try:
            m=bytes_to_long(bytes.fromhex(input()))
        except:
            print("Wrong format")
            exit(0)
        ciphertext=encrypt(m,e,n)
        print("Your Ciphertext is: ")
        print(hex(ciphertext)[2:])
    elif choice.upper()=='G':
        print("Your encrypted flag is:")
        with open('flag.txt','rb') as f:
            flag=bytes_to_long(f.read())
        t=random.randint(2, 2*5)
        for i in range(t):
            ciphertext=encrypt(flag,e,n)
        print(hex(ciphertext)[2:])
    elif choice.upper()=='X':
        print("Exiting...")
        break
    else:
        print("Please enter 'E','G' or 'X'")
