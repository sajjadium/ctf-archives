import numpy as np
from random import choice

A = np.array([[1, 7, 13, 19, 25, 31],
            [2, 8, 14, 20, 26, 32],
            [3, 9, 15, 21, 27, 33],
            [4, 10, 16, 22, 28, 34],
            [5, 11, 17, 23, 29, 35],
            [6, 12, 18, 24, 30, 36]])
B = np.array([[36, 30, 24, 18, 12, 6],
            [35, 29, 23, 17, 11, 5],
            [34, 28, 22, 16, 10, 4],
            [33, 27, 21, 15, 9, 3],
            [32, 26, 20, 14, 8, 2],
            [31, 25, 19, 13, 7, 1]])
C = np.array([[31, 25, 19, 13, 7, 1],
            [32, 26, 20, 14, 8, 2],
            [33, 27, 21, 15, 9, 3],
            [34, 28, 22, 16, 10, 4],
            [35, 29, 23, 17, 11, 5],
            [36, 30, 24, 18, 12, 6]])
D = np.array([[7, 1, 9, 3, 11, 5],
            [8, 2, 10, 4, 12, 6],
            [19, 13, 21, 15, 23, 17],
            [20, 14, 22, 16, 24, 18],
            [31, 25, 33, 27, 35, 29],
            [32, 26, 34, 28, 36, 30]])
E = np.array([[2, 3, 9, 5, 6, 12],
            [1, 11, 15, 4, 29, 18],
            [7, 13, 14, 10, 16, 17],
            [20, 21, 27, 23, 24, 30],
            [19, 8, 33, 22, 26, 36],
            [25, 31, 32, 28, 34, 35]])
permutes = [A, B, C, D, E]


def getRandomKey():
    letters = "abcdefghijklmnopqrstuvwxy"
    key = choice(letters)
    for i in range(1,11):
        oldletter = key[i-1]
        newletter = choice(letters)
        oldletterNum = ord(oldletter)-97
        newletterNum = ord(newletter)-97
        while (newletterNum//5 == oldletterNum//5 or newletterNum%5 == oldletterNum % 5) or newletter in key:
            newletter = choice(letters)
            newletterNum = ord(newletter)-97
        key+=newletter
    return key


def permute(blockM, count):
    finalBlockM = np.zeros((6,6))
    for i in range(6):
        for j in range(6):
            index = int(permutes[count][i,j]-1)
            finalBlockM[i,j] = blockM[index//6, index%6]
    return finalBlockM


def add(blockM, count):
    if count == 0:
        for i in range(6):
            for j in range(6):
                if (i+j)%2 == 0:
                    blockM[i,j] +=1
    elif count == 1:
        blockM[3:,3:] = blockM[3:,3:]+blockM[:3,:3]
    elif count == 2:
        blockM[:3,:3] = blockM[3:,3:]+blockM[:3,:3]
    elif count == 3:
        blockM[3:,:3] = blockM[3:,:3]+blockM[:3,3:]
    else:
        blockM[:3,3:] = blockM[3:,:3]+blockM[:3,3:]
    return np.mod(blockM, 3)


def encrypt(plaintext, key):
    plaintext += "x"*((12-len(plaintext)%12)%12)
    blocks = [plaintext[12*i:12*(i+1)] for i in range(0,len(plaintext)//12)]
    keyNums = [ord(key[i])-97 for i in range(len(key))]
    resultLetters = ""

    #do the block permutations and additions
    for block in blocks:
        #make 6 by 6 matrix
        blockM =np.zeros((6,6))
        for (i,letter) in enumerate(block[0:6]):
            letterNum = ord(letter)-96
            blockM[0,i] = letterNum//9
            blockM[1,i] = (letterNum%9)//3
            blockM[2,i] = letterNum%3
        for (i,letter) in enumerate(block[6:]):
            letterNum = ord(letter)-96
            blockM[3,i] = letterNum//9
            blockM[4,i] = (letterNum%9)//3
            blockM[5,i] = letterNum%3

        
        #scramble matrix
        for keyNum in keyNums:
            blockM = permute(blockM,(keyNum//5)%5)
            blockM = add(blockM, keyNum%5)
        

        #get resulting letters from matrix
        for i in range(6):
            resultLetterNum = int(9*blockM[i,0]+3*blockM[i,1]+blockM[i,2])
            if resultLetterNum == 0:
                resultLetters += "0"
            else:
                resultLetters += chr(resultLetterNum+96)
        for i in range(6):
            resultLetterNum = int(9*blockM[i,3]+3*blockM[i,4]+blockM[i,5])
            if resultLetterNum == 0:
                resultLetters += "0"
            else:
                resultLetters += chr(resultLetterNum+96)

    #rearrange ciphertext according to the key
    reducedKeyNums = []
    [reducedKeyNums.append(x) for x in keyNums if x not in reducedKeyNums]
    letterBoxes = [[] for i in reducedKeyNums]
    finalEncryptedText = ""
    for i in range(len(resultLetters)):
        letterBoxes[i%len(reducedKeyNums)].append(resultLetters[i])
    for i in range(len(reducedKeyNums)):
        nextLowest = reducedKeyNums.index(min(reducedKeyNums))
        reducedKeyNums[nextLowest] = 27
        for letter in letterBoxes[nextLowest]:
            finalEncryptedText+=letter

    return(finalEncryptedText)

if __name__ == "__main__":
    plaintext =  input("What would you like to encrypt?\n")
    plaintextList = [letter.lower() for letter in plaintext if letter.isalpha()]
    plaintext = ""
    for letter in plaintextList:
        plaintext += letter
    key = input("Enter the encryption key. Leave blank to randomly generate.\n")
    if key == "":
        key = getRandomKey()
        print(f"Your key is: {key}")
    print(encrypt(plaintext, key))

