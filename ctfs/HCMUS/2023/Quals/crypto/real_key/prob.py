from Crypto.Cipher import AES
from Crypto.Util.number import getRandomInteger
from Crypto.Util.Padding import pad
import numpy as np




def gen_key():
    key = getRandomInteger(128).to_bytes(16, 'big')
    while b'\0' in key: key = getRandomInteger(128).to_bytes(16, 'big')
    mat = [[i for i in key[k:k+4]] for k in range(0, 16, 4)]
    return key, mat

def f(mat):
    """Make the key wavy"""
    N = 1600
    T = 1/800
    x = np.linspace(0, N*T, N)
    ys = [np.sum(np.array([.5**i * np.sin(n * 2 * np.pi * x) for i, n in enumerate(b)]), axis=0).tolist() for b in mat]
    return ys

def check_good_mat(mat):
    for row in mat:
        for i in range(4):
            if row[i] > 255: return False
            for j in range(i + 1, 4):
                if -1 == row[i] - row[j] or row[i] - row[j] == 1 or row[i] == row[j]: return False
    return True


                 
key, mat = gen_key()
while not check_good_mat(mat):
    key, mat = gen_key()

ys = f(mat)
FLAG = pad(b'FLAG{real_flag_goes_here}', 16)
cip = AES.new(key, AES.MODE_CBC)
iv = cip.iv

ciphertext = cip.encrypt(FLAG)

# The stuff which will be given
with open('output.txt', 'w') as ofile:
    print(ys, file=ofile)
with open('ciphertext.bin', 'wb') as ofile:
    ofile.write(iv)
    ofile.write(ciphertext)