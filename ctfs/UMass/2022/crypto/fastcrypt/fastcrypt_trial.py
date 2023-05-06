#!/usr/bin/env python3
#
# Polymero
#

# Imports
import os

# Local imports
with open("flag.txt",'rb') as f:
    FLAG = f.read()
    f.close()

HDR = r"""|
|   __________             ______________                      _____ 
|   ___  ____/_____ _________  /__  ____/___________  ___________  /_
|   __  /_   _  __ `/_  ___/  __/  /    __  ___/_  / / /__  __ \  __/
|   _  __/   / /_/ /_(__  )/ /_ / /___  _  /   _  /_/ /__  /_/ / /_  
|   /_/      \__,_/ /____/ \__/ \____/  /_/    _\__, / _  .___/\__/  
|    the Fastest Encryptor in the Digital West /____/  /_/           
|"""

MSG = r"""|
|
|   This is a free trial version of FastCrypt(tm).
|   To unlock the full version please provide your license key.
|   
|   To show FastCrypt(tm) is safe, we include an encrypted license key under a random key:"""

# Class
class FastCrypt:
    # Box created from PI decimals (in byte form), so nothing up our sleeve.
    PI_BOX = [[36, 63, 106, 136, 133, 163, 8, 211, 19, 25, 138, 46, 3, 112, 115, 68],
              [164, 9, 56, 34, 41, 159, 49, 208, 250, 152, 236, 78, 108, 137, 69, 40],
              [33, 230, 119, 190, 84, 102, 207, 52, 233, 12, 192, 172, 183, 201, 124, 80],
              [221, 132, 213, 181, 71, 23, 146, 22, 217, 121, 251, 27, 209, 11, 166, 223],
              [47, 253, 114, 219, 26, 184, 225, 175, 237, 38, 126, 150, 186, 144, 241, 44],
              [127, 153, 161, 179, 145, 247, 1, 242, 226, 142, 252, 99, 105, 32, 216, 113],
              [87, 88, 254, 244, 147, 61, 13, 149, 116, 143, 182, 139, 205, 130, 21, 74],
              [238, 123, 29, 194, 90, 89, 156, 48, 57, 42, 96, 197, 176, 35, 240, 202],
              [65, 24, 239, 220, 58, 14, 158, 30, 62, 215, 193, 189, 75, 39, 120, 218],
              [85, 92, 37, 243, 170, 171, 148, 72, 98, 232, 20, 64, 16, 180, 204, 17],
              [206, 134, 111, 188, 43, 169, 93, 246, 155, 135, 214, 51, 122, 50, 83, 129],
              [59, 107, 185, 196, 191, 97, 128, 117, 177, 2, 235, 101, 15, 109, 131, 66],
              [4, 200, 31, 94, 198, 104, 154, 103, 81, 160, 210, 167, 110, 228, 118, 67],
              [140, 125, 165, 195, 224, 86, 54, 6, 55, 10, 18, 234, 73, 7, 212, 222],
              [227, 76, 151, 79, 178, 82, 203, 168, 95, 0, 248, 60, 173, 5, 187, 255],
              [91, 45, 77, 174, 199, 100, 28, 229, 162, 245, 157, 53, 231, 249, 70, 141]]
    PI_BOX = [i for j in PI_BOX for i in j]

    def __init__(self):
        # Key for encrypting a valid license key
        self.secret_key = os.urandom(16)
        self.license = 'License key: ' + os.urandom(8).hex()

    def pad(self, msg):
        if type(msg) == str:
            msg = msg.encode()
        return msg + chr(32-len(msg)%32).encode() * (32-len(msg)%32)

    def unpad(self, msg):
        numpad = msg[-1]
        if numpad > 32:
            return False
        pdn = msg[-numpad:]
        msg = msg[:-numpad]
        if pdn != numpad*chr(numpad).encode():
            return False
        return msg

    def sub(self, block):
        return [self.PI_BOX[i] for i in block]

    def perm(self, block):
        bitblock = list('{:0256b}'.format(int(bytes(block).hex(),16)))
        permbits = [bitblock[self.PI_BOX[i]] for i in range(256)]
        return [int(''.join(permbits[i:i+8]),2) for i in range(0,256,8)]

    def encrypt_block(self, block, keybits):
        for keybit in keybits:
            if keybit == 1:
                block = self.sub(block)
            if keybit == 0:
                block = self.perm(block)
        return block

    def encrypt(self, msg, key=None, iv=None):
        if key is None or key == '':
            key = self.secret_key
        assert len(key) == len(self.secret_key)
        if iv is None:
            iv = os.urandom(len(self.secret_key)//4)
        keybits = [int(i) for i in list('{:0{nk}b}'.format(int(key.hex(),16),nk=len(self.secret_key)*8))]
        ivindex = [int(i,16) for i in list(iv.hex())]
        keybits += [keybits[ivindex[i]+16*i] for i in range(len(iv)*2)]
        blocks = self.pad(msg)
        blocks = [list(blocks[i:i+32]) for i in range(0,len(blocks),32)]
        ciphertext = []
        for b,block in enumerate(blocks):
            ciphertext += self.encrypt_block(block, keybits)
        return (iv + bytes(ciphertext)).hex()


# Challenge
FC = FastCrypt()

print(HDR)
print(MSG)
print("|   {}".format(FC.encrypt(FC.license)))

while True:

    try:

        print("|\n|  Menu:")
        print("|   [1] Encrypt (trial)")
        print("|   [2] Enter license key")

        choice = input("|\n|   >> ")

        if choice == '1':

            print("|\n|  What would you like to encrypt? [enter no iv to use a random iv]:")

            iv  = input("|\n|   >> Iv : ")
            msg = input("|   >> Msg: ")

            try:

                cip = FC.encrypt(msg.encode(), iv=bytes.fromhex(iv))

            except:

                cip = FC.encrypt(msg.encode())

            print("|\n|  Encrypted message:\n|   {}".format(cip))

        if choice == '2':

            print("|\n|  Enter a valid license key:")

            license = input("|\n|   >> ")

            if license == FC.license[-16:]:
                print("|\n|  Thank you for purchasing FastCrypt(tm), please enjoy this welcome gift!")
                print('|   {}'.format(FLAG))
                print('|')
                exit(0)

            else:
                print("|\n|  Invalid license key!")

    except KeyboardInterrupt:
        print("\n|\n|  Thank you for using FastCrypt(tm)!\n|\n")
        exit(0)

    except:
        print("|\n|\n|  Something went wrong, please try again.")
