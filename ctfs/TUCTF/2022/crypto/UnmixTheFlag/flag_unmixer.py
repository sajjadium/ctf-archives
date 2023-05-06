import string

upperFlag = string.ascii_uppercase[:26]
lowerFlag = string.ascii_lowercase[:26]
MIN_LETTER = ord("a")
MIN_CAPLETTER = ord("A")

def mix(oneLetter,num):

    if(oneLetter.isupper()):
        word = ord(oneLetter)-MIN_CAPLETTER
        shift = ord(num)-MIN_CAPLETTER
        return upperFlag[(word + shift)%len(upperFlag)]
    if(oneLetter.islower()):
        word = ord(oneLetter)-MIN_LETTER
        shift = ord(num)-MIN_LETTER
        return lowerFlag[(word + shift)%len(upperFlag)]

def puzzled(puzzle):
    toSolveOne = ""
    for letter in puzzle:
    
        if (letter.isupper()):
            binary ="{0:015b}".format(ord(letter))

            toSolveOne += upperFlag[int(binary[:5],2)]
            toSolveOne += upperFlag[int(binary[5:10],2)]
            toSolveOne += upperFlag[int(binary[10:],2)]

        elif(letter.islower()):
            six = "{0:02x}".format(ord(letter))
            toSolveOne += lowerFlag[int(six[:1],16)]
            toSolveOne += lowerFlag[int(six[1:],16)]
        elif(letter == "_"):
            toSolveOne += "CTF"  
    return toSolveOne   

    
flag = "Figure it Out! :)"
numShift = "??"
mixed = ""

assert all([x in lowerFlag for x in numShift])
assert len(numShift) == 1

encoding = puzzled(flag)
print(encoding)
for count, alpha in enumerate(encoding):
    mixed += mix(alpha, numShift)

print(mixed)






    

        






