#!/usr/bin/python3
from hashlib import *
from string import hexdigits as chars
chars = chars[:16]
from tqdm import *

def brute(known, H):
    for i in tqdm(chars):
        for j in chars:
            for k in chars:
                for l in chars:
                    for m in chars:
                        for n in chars:
                            if sha256((known+i+j+k+l+m+n).encode()).hexdigest() == H:
                                return (i+j+k+l+m+n)


if __name__=="__main__":
    known = input("known: ")
    H = input("hash: ")
    print(brute(known, H))
