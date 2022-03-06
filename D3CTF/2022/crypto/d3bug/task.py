from Crypto.Util.number import *
from secret import flag
assert flag.startswith("D3CTF{")
assert flag.endswith("}")
message = bytes_to_long(flag[6:-1])
assert message < 2**64
mask = 0b1010010000001000000010001001010010100100000010000000100010010100

def lfsr_MyCode(R,mask):
    output = (R << 1) & 0xffffffffffffffff
    i = (R ^ mask) & 0xffffffffffffffff
    lastbit = 0
    while i != 0:
        lastbit ^= (i & 1)
        i = i>>1
    output ^= lastbit
    return (output,lastbit)

def lfsr_CopiedfromInternet(R,mask):
    output = (R << 1) & 0xffffffffffffffff
    i = (R & mask) & 0xffffffffffffffff
    lastbit = 0
    while i != 0:
        lastbit ^= (i & 1)
        i = i>>1
    output ^= lastbit
    return (output,lastbit)

f=open("standardResult","w")
R=message
for i in range(35):
    (R, out) = lfsr_CopiedfromInternet(R,mask)
    f.write(str(out))
f.close()

f=open("myResult","w")
R=message
for i in range(35):
    (R, out) = lfsr_MyCode(R,mask)
    f.write(str(out))
f.close()

#Why are the results always different?!!
#Can you help me debug my code? QAQ