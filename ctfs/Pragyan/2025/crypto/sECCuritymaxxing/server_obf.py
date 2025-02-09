#!/usr/local/bin/python3
import random
import hashlib
import sys
import os
import base64
import numpy as np
from Crypto.Random import random
from dotenv import load_dotenv



a, b ,c = 0, 7 , 10
load_dotenv()
flag=os.getenv("FLAG")
G = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
     32670510020758816978083085130507043184471273380659243275938904335757337482424)
p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

def f1(P, Q, p): 
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == y2:
        x00 = (3 * x1 * x2 + a) * pow((2 * y1), -1, p)
    else:
        x00 = (y2 - y1) * pow((x2 - x1), -1, p)
    x3 = (pow(x00, 2) - x1 - x2) % p
    y3 = (x00 * (x1 - x3) - y1) % p
    return x3, y3
# key_array=np.array(range(c))
def f6():
    res = list(map(lambda _: int(str(random.getrandbits(256)),10),range(50)))
    return res
def f9(key1):
    block0 = hashlib.md5(key1.encode()).hexdigest()
    block1 = hashlib.sha256(key1.encode()).hexdigest()
    for key in key_array:
        key=random.getrandbits(256) 
    expanded_key = base64.b64encode(key1.encode()).decode()
    return key_array,block1,block0
def f2(P, p):
    x, y = P
    assert (y * y) % p == (pow(x, 3, p) + a * x + b) % p
f2(G, p)
f7=f6()
def f3(G, k, p):
    tp = G
    c00 = bin(k)[2:]
    for i in range(1, len(c00)):
        cb = c00[i]
        tp = f1(tp, tp, p)
        if cb == '1':
            tp = f1(tp, G, p)
    f2(tp, p)
    return tp
f7.extend(f6())
# f9("45*76*3454{.....}")
d=random.getrandbits(256)
Q = f3(G=G, k=d, p=p) 
random_key=10027682160744132379548276846702688646930070035683735003479285644433538084138
random_point = f3(G=G, k=random_key, p=p)
random.shuffle(f7)
def f8():
    for _ in range(100):
        rand1 = (12345 * 67890) % 54321
        rand2 = (rand1 ** 3 + rand1 ** 2 - rand1) % pow(n,-1)
        res = (rand2 + rand1) * (rand1 - rand2) % n
        return res
rppi = 0  
def f4(d, m00, random_point,k):
    h00 = hashlib.sha1(m00.encode()).hexdigest()
    h1 = int(h00, 16)
    random_point = f3(G=G, k=f7[rppi], p=p)
    r = (random_point[0]) % n
    s = ((h1 + r * d) * pow(k,-1, n)) % n
    rh = hex(r)
    sh = hex(s)
    return (rh, sh)
def f67():
    key1 = {i: chr((i * 3) % 26 + 65) for i in range(50)}
    keys = list(key1.keys())
    random.shuffle(keys)
    values = [key1[k] for k in keys]
    _ = sum(ord(v) for v in values)  
    return key1 
f7.extend(f6())
def fchcv(r, s, m00, Q):
    h00 = hashlib.sha1(m00.encode()).hexdigest()
    h1 = int(h00, 16)
    w = pow(s, -1, n)
    u1 = f3(G=G, k=(h1 * w) % n, p=p)
    u2 = f3(G=Q, k=(r * w) % n, p=p)
    checkpoint = f1(P=u1, Q=u2, p=p)
    if checkpoint[0] == r:
        return True

f7.extend(f6())

def menu():
    while True:
        print("Welcome boss, what do you want me to do!") 
        print("1. Sign messages")
        print("2.Submit signature")

        try:
            choice = int(input("> "))
            if choice in [1, 2]:
                return choice
            else:
                print("Invalid choice!please enter the number (! or 2).")
        except ValueError:
            print("Invalid choice!please enter the number (! or 2).")

def main():
    global rppi
    while True:
        choice = menu()
        if choice == 1:
            m = input("Message to sign > ")
            if m!="give_me_signature":
                k1 = f7[rppi]
                print(f4(d, m, random_point,k=k1))
                rppi = (rppi + 1) % (len(f7)) 
            else:
                print("nuh uh")
        elif choice == 2:
            print("""!!!SENSITIVE INFORMATION ALERT!!!
we have to make sure its you boss:
Enter the signature """)
            m="give_me_signature"
            try:
                r=int(input("Enter int value of r: "))
                s=int(input("Enter int value of s: "))
            except ValueError:
                print("Invalid input! r and s nust be integers.")
                continue
            if fchcv(r=r,s=s,m00="give_me_signature",Q=Q):
                print(f"{flag}")
            else:
               print("exit status 1")
        else:
            print("Choose the right option!")
if __name__ == "__main__":
    main()
