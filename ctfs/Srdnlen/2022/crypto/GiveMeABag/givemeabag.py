from random import randint
from math import gcd
from secret import FLAG

BIN_LEN = 240

class MHK:

    def __init__(self):

        self.b = []
        self.w = []
        self.q = 0
        self.r = 0

        self.genKeys()


    def genKeys(self):

        k = 30

        self.w.append(randint(1,2**(k//2)))
        sum = self.w[0]

        for i in range(1, BIN_LEN):
            self.w.append(sum + randint(1, 2**k))
            sum += self.w[i]

        self.q = sum + randint(1, 2**k)

        while True:
            self.r = sum + randint(1, 2**k)
            if gcd(self.r,self.q) == 1:
                break

        for i in range(BIN_LEN):
            self.b.append((self.w[i]*self.r)%self.q)


    def encrypt(self, plaintext):

        msgBin = ''.join('{:08b}'.format(b) for b in plaintext.encode('utf8'))

        if len(msgBin) < BIN_LEN:
            msgBin = msgBin.zfill(BIN_LEN)

        ciphertext = 0
        for i in range(len(msgBin)):
            ciphertext += self.b[i]*int(msgBin[i],2)

        return str(ciphertext)


    def decrypt(self, ciphertext):

        plaintext = ''
        ciphertext = int(ciphertext)

        new_ciphertext = (ciphertext* pow(self.r,-1,self.q) )%self.q

        for i in range(len(self.w)-1,-1,-1):
            if self.w[i] <= new_ciphertext:
                new_ciphertext -= self.w[i]
                plaintext += '1'
            else:
                plaintext += '0'
        
        return int(plaintext[::-1], 2).to_bytes((len(plaintext) + 7) // 8, 'big').decode()


if __name__ == "__main__":

    crypto = MHK()
    encrypted = crypto.encrypt(FLAG)

    file=open('./output.txt','w+')
    file.writelines('b = '+ str(crypto.b))
    file.writelines('\nw = '+ str(crypto.w[:2]))
    file.writelines('\nc = '+ str(encrypted))
    file.close()
