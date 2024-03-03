import random
from Crypto.Cipher import AES
import time
import os
from flag import flag

m = 288493873028852398739253829029106548736

a = int(time.time())

b = a%16

s = random.randint(1,m-1)

class LCG:
    def __init__(self, a, b, m, seed):
        self.a = a
        self.b = b
        self.m = m
        self.state = seed
        self.counter = 0

    def next_state(self):
        ret = self.state
        self.state = (self.a * self.state + self.b) % self.m
        return ret

class SuperAES:
    def __init__(self,key,lcg):
        self.aes = AES.new(key,AES.MODE_ECB)
        self.lcg = lcg

    def encrypt(self,plaintext):
        ciphertext = b""
        for i in range(0,len(plaintext),16):
            ciphertext += self.encrypt_block(plaintext[i:i+16])

        return ciphertext

    def encrypt_block(self,block):
        keystream = self.aes.encrypt(int(self.lcg.next_state()).to_bytes(16,"big"))
        return bytes([k^b for k,b in zip(keystream,block)])

assert len(flag) == 33
assert flag.startswith(b"GCC{")

key = os.urandom(32)

cipher = SuperAES(key,LCG(a,b,m,s))

times = int(input("how many times do you want the flag ?"))

assert times < 50

print(cipher.encrypt(flag*times).hex())