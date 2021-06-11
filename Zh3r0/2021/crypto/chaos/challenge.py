from secret import flag
def ROTL(value, bits, size=32):
    return ((value % (1 << (size - bits))) << bits) | (value >> (size - bits))

def ROTR(value, bits, size=32):
    return ((value % (1 << bits)) << (size - bits)) | (value >> bits)

def pad(pt):
    pt+=b'\x80'
    L = len(pt)
    to_pad = 60-(L%64) if L%64 <= 60 else 124-(L%64)
    padding = bytearray(to_pad) + int.to_bytes(L-1,4,'big')
    return pt+padding

def hash(text:bytes):
    text = pad(text)
    text = [int.from_bytes(text[i:i+4],'big') for i in range(0,len(text),4)]
    M = 0xffff
    x,y,z,u = 0x0124fdce, 0x89ab57ea, 0xba89370a, 0xfedc45ef
    A,B,C,D = 0x401ab257, 0xb7cd34e1, 0x76b3a27c, 0xf13c3adf
    RV1,RV2,RV3,RV4 = 0xe12f23cd, 0xc5ab6789, 0xf1234567, 0x9a8bc7ef
    for i in range(0,len(text),4):
        X,Y,Z,U = text[i]^x,text[i+1]^y,text[i+2]^z,text[i+3]^u
        RV1 ^= (x := (X&0xffff)*(M - (Y>>16)) ^ ROTL(Z,1) ^ ROTR(U,1) ^ A)
        RV2 ^= (y := (Y&0xffff)*(M - (Z>>16)) ^ ROTL(U,2) ^ ROTR(X,2) ^ B)
        RV3 ^= (z := (Z&0xffff)*(M - (U>>16)) ^ ROTL(X,3) ^ ROTR(Y,3) ^ C)
        RV4 ^= (u := (U&0xffff)*(M - (X>>16)) ^ ROTL(Y,4) ^ ROTR(Z,4) ^ D)
    for i in range(4):
        RV1 ^= (x := (X&0xffff)*(M - (Y>>16)) ^ ROTL(Z,1) ^ ROTR(U,1) ^ A)
        RV2 ^= (y := (Y&0xffff)*(M - (Z>>16)) ^ ROTL(U,2) ^ ROTR(X,2) ^ B)
        RV3 ^= (z := (Z&0xffff)*(M - (U>>16)) ^ ROTL(X,3) ^ ROTR(Y,3) ^ C)
        RV4 ^= (u := (U&0xffff)*(M - (X>>16)) ^ ROTL(Y,4) ^ ROTR(Z,4) ^ D)
    return int.to_bytes( (RV1<<96)|(RV2<<64)|(RV3<<32)|RV4 ,16,'big')

try:
    m1 = bytes.fromhex(input("input first string to hash : "))
    m2 = bytes.fromhex(input("input second string to hash : "))
    if m1!=m2 and hash(m1)==hash(m2):
        print(flag)
    else:
        print('Never gonna give you up')
except:
    print('Never gonna let you down')
