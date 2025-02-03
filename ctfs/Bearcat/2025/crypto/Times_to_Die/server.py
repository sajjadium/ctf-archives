import sys
import socket
import random
from time import time

def xor(bytes1, bytes2):    
    return bytes(a ^ b for a, b in zip(bytes1, bytes2))

def pad(plaintext, length):
    pad_len = length - (len(plaintext)%length)
    return plaintext + bytes([pad_len]*pad_len)

def encrypt(plaintext):
    key = int(time()*2**16)
    random.seed(key)
    plaintext = pad(plaintext,4)
    blocks = []
    for i in range(0,len(plaintext),4):
        ct_block = xor(plaintext[i:i+4],random.randbytes(4))
        blocks.append(ct_block)
    ciphertext = b''.join(blocks)
    return ciphertext

def main():
    if len(sys.argv) < 2:
        print('Usage: server.py <ip>')
        return 1
    ip = sys.argv[1]

    with open('flag.txt','rb') as fil:
        flag = fil.read()
    assert flag.startswith(b'BCCTF{')
    flag_enc = encrypt(flag)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 1337))
    client.sendall(flag_enc)
    client.close()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())