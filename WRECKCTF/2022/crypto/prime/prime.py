#!/usr/local/bin/python

import random
import math
with open ("flag.txt", "r") as f:
    flag = f.read()
n = int(input(">> "))
n_len = n.bit_length()
if n_len<1020 or n_len>1028:
    print("no.")
    quit()
for i in range(2,1000):
    if n%i==0:
        print("no.")
        quit()
if all([pow(random.randrange(1,n), n-1, n) == 1 for i in range(256)]):
    a = []
    for _ in range(70):
        a.append(int(input(">> ")))
    if all([n%i==0 for i in a]):
        for i in range(len(a)):
            for j in range(i+1, len(a)):
                if math.gcd(a[i],a[j])!=1:
                    print(a[i],a[j])
                    print("no.")
                    quit()
        print(flag)
    else:
        print("no.")
        quit()
