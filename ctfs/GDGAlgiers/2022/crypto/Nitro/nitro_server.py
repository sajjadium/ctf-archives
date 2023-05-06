#!/usr/bin/sage

from sage.all import *
from nitro import Nitro

with open("flag.txt","r") as f:
    flag = f.readline()

assert len(flag)==32

def str2bin(s):
    return ''.join(bin(ord(i))[2:].zfill(8) for i in s)

def main():
    print("**********       NITRO ORCALE      **********")
    print("   Welcome to the nitro oracle   ")
    print("After getting inspired by some encryption services, i tried to built my own server")
    print("My idea is based on using polynomials to make an affine encryption")
    print("Keep in mind that i can only encrypt a specific byte each time")
    print("You can send me the position of the byte and i send the encrypted byte with the used public key ")
    N, p, q, d = 8, 2, 29, 2
    assert gcd(N, q) == 1 and gcd(p, q) == 1 and q > (6 * d + 1) * p
    cipher = Nitro(N, p, q, d)
    print("------------------------------")
    print("|           MENU         |")
    print("|   a) encrypt the ith byte     |")
    print("|   b) exit    |")
    print("------------------------------")


    while True:
        menu= input("choose an option \n")
        try:
            if  menu == "a":
                i = int(input("enter the byte index: "))
                assert i<32
                m = list(str2bin(flag[i]))
                e,h = cipher.encrypt(m)
                print(e)
                print(h)

            elif menu == "b":
                print(" Good Bye !! ")
                exit()

            else:
                print("Error: invalid menu option.")
                raise Exception
        except Exception as ex:
            print("\nSomething went wrong......try again?\n")



if __name__ == "__main__":
    main()
