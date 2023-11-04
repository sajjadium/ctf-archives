import numpy as np
import secrets
import base64
def block_to_words(block):
    # block 128bit byteString
    # words 32 * 4bit int np.array
    # little endian
    divided_blocks = np.array([block[4*i:4*(i+1)] for i in range(4)])
    f = np.frompyfunc(int.from_bytes, 2, 1)
    words = f(divided_blocks,'little')
    return words

def words_to_block(words):
    # words 32 * 4bit int np.array
    # block 128bit byteString
    # little endian
    block = b''.join([i.to_bytes(4,'little') for i in words])
    return block

def rotate_left(x, n):
    # x 32bit int
    # n int
    # rotated 32bit int
    rotated = ((x << n) & 0xffffffff) | (x >> (32 - n))
    return rotated

def rotate_right(x, n):
    # x 32bit int
    # n int
    # rotated 32bit int
    rotated = (x >> n) | ((x << (32 - n)) & 0xffffffff)
    return rotated

primitive_polynomial_g = 0b01101001

def xtime(a):
    # a: 8bit
    # b: 8bit
    if a & 0b10000000 == 0b10000000:
        a = ((a << 1) ^ primitive_polynomial_g) & 0b11111111
    else:
        a <<= 1
    return a

def gmul(a, b):
    # a: 8bit
    # b: 8bit
    # c: 8bit
    c = 0
    for i in range(8):
        if b & 1 == 1:
            c ^= a
        a = xtime(a)
        b >>= 1
    return c

MDS = np.array([
    [0x01, 0xEF, 0x5B, 0x5B],
    [0x5B, 0xEF, 0xEF, 0x01],
    [0xEF, 0x5B, 0x01, 0xEF],
    [0xEF, 0x01, 0xEF, 0x5B]
],dtype='object')

def q0(x):
    # x 8bit int
    # y 8bit int
    t = np.array([
        [0x8,0x1,0x7,0xd,0x6,0xf,0x3,0x2,0x0,0xb,0x5,0x9,0xe,0xc,0xa,0x4],
        [0xe,0xc,0xb,0x8,0x1,0x2,0x3,0x5,0xf,0x4,0xa,0x6,0x7,0x0,0x9,0xd],
        [0xb,0xa,0x5,0xe,0x6,0xd,0x9,0x0,0xc,0x8,0xf,0x3,0x2,0x4,0x7,0x1],
        [0xd,0x7,0xf,0x4,0x1,0x2,0x6,0xe,0x9,0xb,0x3,0x0,0x8,0x5,0xc,0xa]
    ],dtype='object')
    a = np.zeros(5,dtype='object')
    b = np.zeros(5,dtype='object')
    a[0] = (x>>4)%16
    b[0] = x%16
    a[1] = a[0] ^ b[0]
    b[1] = a[0] ^ (((b[0]<<3)&(0b1000)) | b[0]>>1) ^ ((8*a[0])%16)
    a[2] = t[0][a[1]]
    b[2] = t[1][b[1]]
    a[3] = a[2] ^ b[2]
    b[3] = a[2] ^ (((b[2]<<3)&(0b1000)) | b[2]>>1) ^ ((8*a[2])%16)
    a[4] = t[2][a[3]]
    b[4] = t[3][b[3]]
    y = 16*b[4] + a[4]
    return y

def q1(x):
    # x 8bit int
    # y 8bit int
    t = np.array([
        [0x2,0x8,0xb,0xd,0xf,0x7,0x6,0xe,0x3,0x1,0x9,0x4,0x0,0xa,0xc,0x5],
        [0x1,0xe,0x2,0xb,0x4,0xc,0x3,0x7,0x6,0xd,0xa,0x5,0xf,0x9,0x0,0x8],
        [0x4,0xc,0x7,0x5,0x1,0x6,0x9,0xa,0x0,0xe,0xd,0x8,0x2,0xb,0x3,0xf],
        [0xb,0x9,0x5,0x1,0xc,0x3,0xd,0xe,0x6,0x4,0x7,0xf,0x2,0x0,0x8,0xa]
    ],dtype='object')
    a = np.zeros(5,dtype='object')
    b = np.zeros(5,dtype='object')
    a[0] = (x>>4)%16
    b[0] = x%16
    a[1] = a[0] ^ b[0]
    b[1] = a[0] ^ (((b[0]<<3)&(0b1000)) | b[0]>>1) ^ ((8*a[0])%16)
    a[2] = t[0][a[1]]
    b[2] = t[1][b[1]]
    a[3] = a[2] ^ b[2]
    b[3] = a[2] ^ (((b[2]<<3)&(0b1000)) | b[2]>>1) ^ ((8*a[2])%16)
    a[4] = t[2][a[3]]
    b[4] = t[3][b[3]]
    y = 16*b[4] + a[4]
    return y

def h_func(X,L):
    # X 32bit int
    # L 32 * k bit int np.array
    # Y 32bit int
    k=2
    x = np.array([X>>(8*i) &0xff for i in range(4)])
    l = np.zeros((k,4),dtype='object')
    for i in range(k):
        l[i] = np.array([L[i]>>(8*j) &0xff for j in range(4)])
    y = np.zeros((k+1,4) ,dtype='object')
    y[k] = [i for i in x]
    y[0][0] = q1(q0(q0(y[k][0]) ^ l[1][0]) ^ l[0][0])
    y[0][1] = q0(q0(q1(y[k][1]) ^ l[1][1]) ^ l[0][1])
    y[0][2] = q1(q1(q0(y[k][2]) ^ l[1][2]) ^ l[0][2])
    y[0][3] = q0(q1(q1(y[k][3]) ^ l[1][3]) ^ l[0][3])
    z = [0]*4
    for i in range(4):
        for j in range(4):
            z[i] ^= gmul(MDS[i][j],y[0][j])
    Z = 0
    for i in range(4):
        Z += (z[i] << (8*i))
    return Z

def xtime_k(a):
    # a: 8bit
    # b: 8bit
    primitive_polynomial_k = 0b01001101
    if a & 0b10000000 == 0b10000000:
        a = ((a << 1) ^ primitive_polynomial_k) & 0b11111111
    else:
        a <<= 1
    return a

def gmul_k(a, b):
    # a: 8bit
    # b: 8bit
    # c: 8bit
    c = 0
    for i in range(8):
        if b & 1 == 1:
            c ^= a
        a = xtime_k(a)
        b >>= 1
    return c

def key_schedule(key):
    # key 128bit byteSrting
    # Me 32 * 2 bit byteString np.array
    # Mo 32 * 2 bit byteString np.array
    # S 32 * 2 bit byteString np.array
    # keys byteString np.array
    # [key,Me[0],Me[1],Mo[0],Mo[1],S[0],S[1]]
    keys = np.full(7,b"")
    keys[0] = key
    RS = np.array([
        [0x01,0xA4,0x55,0x87,0x5A,0x58,0xDB,0x9E],
        [0xA4,0x56,0x82,0xF3,0x1E,0xC6,0x68,0xE5],
        [0x02,0xA1,0xFC,0xC1,0x47,0xAE,0x3D,0x19],
        [0xA4,0x55,0x87,0x5A,0x58,0xDB,0x9E,0x03]
    ],dtype='object')
    m = np.array([keys[0][4*i:4*(i+1)] for i in range(4)])
    keys[1] = m[0]
    keys[2] = m[2]
    keys[3] = m[1]
    keys[4] = m[3]
    S = np.zeros(2,dtype='object') 
    m2 = np.array([(int.from_bytes(keys[0],'big')>>(8*(15-i))) & 0xff for i in range(16)])
    for i in range(2):
        s = [0]*4
        for j in range(4):
            for k in range(8):
                s[j] ^= gmul_k(RS[j][k],m2[8*i+k])
        for j in range(4):
            S[i] += (s[j] << (8*j))
        keys[6-i] = S[i].to_bytes(4,'little')
    Me = np.full(2,b"")
    Mo = np.full(2,b"")
    S = np.full(2,b"")
    Me[0] = keys[1]
    Me[1] = keys[2]
    Mo[0] = keys[3]
    Mo[1] = keys[4]
    S[0] = keys[5]
    S[1] = keys[6]
    return Me,Mo,S
            
def sbox_with_key(X,i,S):
    # X 8bit int
    # i int 0-3
    # S 32 * 2 bit int
    # Y 8bit int
    k=2
    l = np.zeros((2,4),dtype='object')
    for m in range(k):
        l[m] = [S[m]>>(8*j) &0xff for j in range(4)]
    y = np.zeros((k+1,4) ,dtype='object')
    y[k][i] = X
    if i == 0:
        y[0][0] = q1(q0(q0(y[k][0]) ^ l[1][0]) ^ l[0][0])
    elif i == 1:
        y[0][1] = q0(q0(q1(y[k][1]) ^ l[1][1]) ^ l[0][1])
    elif i == 2:
        y[0][2] = q1(q1(q0(y[k][2]) ^ l[1][2]) ^ l[0][2])
    elif i == 3:
        y[0][3] = q0(q1(q1(y[k][3]) ^ l[1][3]) ^ l[0][3])
    return y[0][i]

def expand_key(Mo,Me):
    # key 128bit byteString
    # keys 32 * 40 bit int
    # little endian
    Mo_int = np.frompyfunc(int.from_bytes, 2, 1)(Mo,'little')
    Me_int = np.frompyfunc(int.from_bytes, 2, 1)(Me,'little')
    keys = []
    rho = 2**24 + 2**16 + 2**8 + 2**0
    A = np.zeros(20,dtype='object')
    B = np.zeros(20,dtype='object')
    for i in range(20):
        A[i]=h_func(2*i*rho,Me_int)
        B[i]=rotate_left(h_func((2*i+1)*rho,Mo_int),8)
    keys = np.zeros(40,dtype='object')
    for i in range(20):
        keys[2*i] = (A[i] + B[i])%(2**32)
        keys[2*i+1] = rotate_left((A[i] + 2*B[i])%(2**32),9)
    return keys

def g_func(X,S):
    # X 32bit int
    # S 32 * 2 bit int
    # Z 32bit int
    x = [X>>(8*i) &0xff for i in range(4)]
    y = [sbox_with_key(x[i],i,S) for i in range(4)]
    z = np.zeros(4,dtype='object')
    for i in range(4):
        for j in range(4):
            z[i] ^= gmul(MDS[i][j],y[j])
    Z = 0
    for i in range(4):
        Z += (z[i] << (8*i))
    return Z
    
def f_func(r0,r1,keys,rounds,S):
    # r0 32bit int
    # r1 32bit int
    # keys 32 * n bit int
    # rounds int 0-15
    # f0 32bit int
    # f1 32bit int
    t0 = g_func(r0,S)
    t1 = g_func(rotate_left(r1,8),S)
    f0 = (t0+t1+keys[2*rounds+8]) % 2**32
    f1 = (t0+2*t1+keys[2*rounds+9]) % 2**32
    return f0,f1

def one_round(words,rounds,keys,S):
    # words 32 * 4bit int
    # rounds int 0-15
    # exchanged_words 32 * 4bit int
    S_int = np.frompyfunc(int.from_bytes, 2, 1)(S,'little')
    f0,f1 = f_func(words[0],words[1],keys,rounds,S_int)
    exchanged_words = [0]*4
    exchanged_words[2] = words[0]
    exchanged_words[3] = words[1]
    exchanged_words[0] = rotate_right(words[2] ^ f0,1)
    exchanged_words[1] = rotate_left(words[3],1) ^ f1
    return exchanged_words

def input_whitening(words,keys):
    # words 32 * 4bit int
    # keys 32 * 4bit int
    # whitened_words 32 * 4bit int
    whitened_words = [0]*4
    for i in range(4):
        whitened_words[i] = words[i] ^ keys[i]
    return whitened_words

def output_whitening(words,keys):
    # words 32 * 4bit int
    # keys 32 * 4bit int
    # whitened_words 32 * 4bit int
    whitened_words = [0]*4
    for i in range(4):
        whitened_words[i] = words[(i+2)%4] ^ keys[i]
    return whitened_words

def twofish_encrypt(block,key):
    # block 128bit byteString
    # key 128bit byteString
    # encrypted_block 128bit byteString
    words = block_to_words(block)
    Me,Mo,S = key_schedule(key)
    keys = expand_key(Mo,Me)
    whitened_words = input_whitening(words,keys[0:4])
    for i in range(16):
        whitened_words = one_round(whitened_words,i,keys,S)
    encrypted_words = output_whitening(whitened_words,keys[4:8])
    encrypted_block = words_to_block(encrypted_words)
    return encrypted_block

def main(flag):
    pad_flag = flag+b'\x00'*(16-len(flag)%16)
    block_length = len(pad_flag)//16
    nonce = int.from_bytes(secrets.token_bytes(12),'big')
    assert block_length <= 2**32
    counter = [int.to_bytes((nonce<<32) + i,16,'big') for i in range(0,block_length)]
    key = secrets.token_bytes(16)
    encrypted_counter = [twofish_encrypt(i,key) for i in counter]
    encrypted_flags = [int.from_bytes(encrypted_counter[i],'big') ^ (int.from_bytes(pad_flag,'big')>>(16*8)*(block_length-1-i))&0xffffffffffffffffffffffffffffffff for i in range(0,block_length)]
    print("nonce = ", nonce)
    print("encrypted_flags = ", encrypted_flags)

if __name__ == '__main__':    
    flag = b"TSGCTF{__REDUCTED__}"
    main(flag)
