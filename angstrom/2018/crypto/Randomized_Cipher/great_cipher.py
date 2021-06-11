#!/usr/bin/python3
#key = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

import random

def genPBox():
    output = list(range(32))
    while output == list(range(32)):
        random.shuffle(output)
    return output

def genSBox():
    output = []
    poss = list(range(16))
    while poss == list(range(16)):
        random.shuffle(poss)
    for i in range(4):
        output.append([0 for i in range(4)])
        for j in range(4):
            output[i][j] = poss[i*4+j]
    return output            

def P(block, permute):
    binary = bin(int.from_bytes(block, byteorder="big"))[2:].zfill(32)
    output = [0 for i in range(32)]
    for i in range(32):
        output[permute[i]] = binary[i]
    return int("".join(output),2).to_bytes(4, byteorder="big")

def S(block, sub):
    blockHex = bytes.hex(block).zfill(8)
    output = ""
    for i in range(8):
        binary = bin(int(blockHex[i],16))[2:].zfill(4)
        outer = int(binary[0] + binary[3],2)
        inner = int(binary[1] + binary[2],2)
        output += hex(sub[i][outer][inner])[2:]
    return bytes.fromhex(output)

def mix(block,key):
    end = b""
    for i in range(len(block)):
        end += (block[i]^key[i]).to_bytes(1, byteorder="big")
    return end

def Eround(block,key,pBox,sBox):
    output = mix(block,key)
    output = S(output,sBox)
    output = P(output,pBox)
    return output

def encrypt(block,keys,rounds,pBox,sBox):
    current = block
    for i in range(rounds-1):
        current = Eround(current,keys[i],pBox,sBox)
    current = mix(current,keys[-1]) #so that last round can"t be reversed
    return current

def oracle(key, inText, rounds, mode, pBox=None, sBox=None):
    #not a very good padding scheme
    while len(inText) % 4 != 0:
        inText += b"\x00"

    if len(key) != 4*rounds: return False

    keys = [key[i:i+4] for i in range(0,len(key),4)]

    if pBox == None: pBox = genPBox()
    print("The permutation box is: ",pBox)
    if sBox == None:
        sBox = []
        for i in range(8):
            sBox.append(genSBox())
            print("Substitution box ",i, " is: " , sBox[i])
    output = b""
    for i in range(0,len(inText),2):
        output += encrypt(inText[i:i+4],keys,rounds,pBox,sBox)

    return bytes.hex(output)

def main():
    while True:
        pt = input("Please enter the hex-encode string you would like to be encrypted: ")
        if len(pt)%2 == 1:
            pt = '0'+pt
        pt = bytes.fromhex(pt)
        ct = oracle(key,pt,8,'encrypt')
        print("Here is the hex-encoded cipher text: " + ct)

main()
