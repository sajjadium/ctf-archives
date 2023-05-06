from present import Present
from Crypto.Util.strxor import strxor
import os, re

class CTRMode():
    def __init__(self, key, nonce=None):
        self.key = key # 20bytes
        self.cipher = DoubleRoundReducedPresent(key)
        if None==nonce:
            nonce = os.urandom(self.cipher.block_size//2)
        self.nonce = nonce # 4bytes
    
    def XorStream(self, data):
        output = b""
        counter = 0
        for i in range(0, len(data), self.cipher.block_size):
            keystream = self.cipher.encrypt(self.nonce+counter.to_bytes(self.cipher.block_size//2, 'big'))
            if b""==keystream:
                exit(1)

            if len(data)<i+self.cipher.block_size:
                block = data[i:len(data)]
            block = data[i:i+self.cipher.block_size]
            block = strxor(keystream[:len(block)], block)
            
            output+=block
            counter+=1
        return output

    def encrypt(self, plaintext):
        return self.XorStream(plaintext)

    def decrypt(self, ciphertext):
        return self.XorStream(ciphertext)

class DoubleRoundReducedPresent():

    def __init__(self, key):
        self.block_size = 8
        self.key_length = 160 # bits
        self.round = 16
        self.cipher0 = Present(key[0:10], self.round)
        self.cipher1 = Present(key[10:20], self.round)
    
    def encrypt(self, plaintext):
        if len(plaintext)>self.block_size:
            print("Error: Plaintext must be less than %d bytes per block" % self.block_size)
            return b""
        return self.cipher1.encrypt(self.cipher0.encrypt(plaintext))
    
    def decrypt(self, ciphertext):
        if len(ciphertext)>self.block_size:
            print("Error: Ciphertext must be less than %d bytes per block" % self.block_size)
            return b""
        return self.cipher0.decrypt(self.cipher1.decrypt(ciphertext))

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), './secret/'))
    from keyfile import key
    from flag import flag

    # load key
    if not re.fullmatch(r'[0-3]+', key):
        exit(1)
    key = key.encode('ascii')

    # load flag
    flag = flag.encode('ascii') # LINECTF{...}

    plain = flag
    cipher = CTRMode(key)
    ciphertext = cipher.encrypt(plain)
    nonce = cipher.nonce

    print(ciphertext.hex())
    print(nonce.hex())

