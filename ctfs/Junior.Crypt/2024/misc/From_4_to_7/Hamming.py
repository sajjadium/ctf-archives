import numpy as np
from random import randint 
from secret import FLAG

mess = FLAG
mess = mess.encode().hex()
inp = [bin(int(h,16))[2:].zfill(4) for h in mess]
inp = [[int(b) for b in c] for c in inp]


imatr = np.array(inp)
print (imatr)

Gen = np.array([[0,1,1,1,0,0,0], 
                [1,0,1,0,1,0,0], 
                [1,1,0,0,0,1,0], 
                [1,1,1,0,0,0,1]])

code = np.mod(np.dot(imatr, Gen), 2)
scode = "".join(["".join([str(x) for x in c]) for c in code])

print ("".join([hex(int(scode[i:i+8],2))[2:].zfill(2) for i in range(0, len(scode),8)]))



for i in range(0, code.shape[0]):
    ind = randint(0, 2 * code.shape[1])
    if ind < code.shape[1]:
        code[i, ind] = code[i, ind] ^ 1


ecode = "".join(["".join([str(x) for x in c]) for c in code])
print (len(ecode), ecode)

print ("".join([hex(int(ecode[i:i+8],2))[2:].zfill(2) for i in range(0, len(ecode),8)]))
