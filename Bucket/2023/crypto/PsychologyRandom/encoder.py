seedKey = [] # set of 4 human random numbers between 0 and 255 inclusive
addKey =  humanRandomGenerator(1,10) # human random number between 1 and 10 inclusive
for i in range(4):
    seedKey.append(humanRandomGenerator(0, 255))

with open("flag.txt", "rb") as f:
    flag = f.read()

encryptedFlag = bytearray()
for i in range(len(flag)):
    encryptedFlag.append(flag[i] ^ seedKey[i%4])
    seedKey[i%4] = (seedKey[i%4] + addKey) % 255
