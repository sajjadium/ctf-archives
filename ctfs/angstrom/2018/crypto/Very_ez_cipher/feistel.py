#!/usr/bin/python3
#key = 0xXXXXXXXXXXXXX
size = len(bin(key)[2:])

def F(left, right, key):
    newR = (((right^key)>>3) + (((right^key)&7)<<(size//2-3))) ^ 0x3ffffff
    return (right, left^newR)

def encrypt(block, key):
    key0 = key>>size//2
    key1 = key & int('1'*(size//2),2)
    L = block>>size//2
    R = block & int('1'*(size//2),2)
    for i in range(128):
        L,R = F(L,R,key0)
        L,R = F(L,R,key1)


    return (L<<size//2)+R

while True:
    pt = int(input("Enter a block of plaintext (as hex, at most 13 chars) that you would like to encrypt: ")[:9],16)
    ct = encrypt(pt,key)
    print("Here is the ciphertext:", (hex(ct)[2:]).zfill(size//4))
