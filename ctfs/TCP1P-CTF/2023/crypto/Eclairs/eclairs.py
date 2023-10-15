from Crypto.Util.number import getPrime, bytes_to_long
from sympy.ntheory.modular import crt
from libnum.ecc import *
import random
import time

while (p:=getPrime(256)) % 4 != 3: pass
while (q:=getPrime(256)) % 4 != 3: pass
e = 3
n = p*q
a = getPrime(256)
b = getPrime(256)
E = Curve(a, b, n)
flag = bytes_to_long(open("flag.txt", "rb").read())

def sqrt_mod(a):
    assert p % 4 == 3
    assert q % 4 == 3
    r = int(crt([p,q],[pow(a,(p+1)//4,p), pow(a,(q+1)//4,q)])[0])
    n = p*q
    if pow(r,2,n) == a % n:
        return r
    return False

def lift_x(x):
    y = sqrt_mod(x**3 + a*x + b)
    if y:
        return (x, y)
    return False


def find_coordinates(x):
    P = lift_x(x)
    if P:
        x,y = P
        return (pow(x,e,n), pow(y,e,n))
    return False

def captcha():
    while True:
        x = random.randint(1, n)
        P = lift_x(x)
        if P : break
    k = random.randint(1,n)
    print("HOLD UP!!!!")
    print("YOU ARE ABOUT TO DO SOMETHING VERY CONFIDENTIAL")
    print("WE NEED TO MAKE SURE THAT YOU ARE NOT A ROBOT")
    print(f"Calculate {k} X {P}")
    ans = input("Answer: ")
    return ans == str(E.power(P,k))
    

while True:
    print("1. Check out my cool curve")
    print("2. Get flag")
    print("3. Exit")
    choice = input(">> ")

    if choice == "1":
        print("This point is generated using the following parameter:")
        # encrypted because I don't want anyone to steal my cool curve >:(
        print(pow(a,e,n))
        print(pow(b,e,n))
        x = int(input("x: "))
        P = find_coordinates(x)
        if P:
            print(P)
        else:
            print("Not found :(")

    elif choice == "2":
        if captcha():
            print(pow(flag, e, n))
        else:
            print("GO AWAY!!!")
            exit()
    elif choice == "3":
        exit()
    else:
        print("??")
        exit()