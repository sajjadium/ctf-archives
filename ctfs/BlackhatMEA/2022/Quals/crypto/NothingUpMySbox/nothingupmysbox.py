#!/usr/local/bin/python
#
# Polymero
#

# Imports
import os, time
from secrets import randbelow
from hashlib import sha256

# Local imports
FLAG = os.environ.get('FLAG').encode()


class NUMSBOX:
    def __init__(self, seed, key):
        self.sbox = self.gen_box('SBOX :: ' + seed)
        self.pbox = self.gen_box(str(time.time()))
        self.key = key

    def gen_box(self, seed):
        box = []
        i = 0
        while len(box) < 16:
            i += 1
            h = sha256(seed.encode() + i.to_bytes(2, 'big')).hexdigest()
            for j in h:
                b = int(j, 16)
                if b not in box:
                    box += [b]
        return box
    
    def subs(self, x):
        return [self.sbox[i] for i in x]
    
    def perm(self, x):
        return [x[i] for i in self.pbox]
    
    def kxor(self, x, k):
        return [i ^ j for i,j in zip(x, k)]
    
    def encrypt(self, msg):
        if len(msg) % 16:
            msg += (16 - (len(msg) % 16)) * [16 - (len(msg) % 16)]
        blocks = [msg[i:i+16] for i in range(0, len(msg), 16)]
        cip = []
        for b in blocks:
            x = self.kxor(b, self.key)
            for _ in range(4):
                x = self.subs(x)
                x = self.perm(x)
                x = self.kxor(x, self.key)
            cip += x
        return ''.join([hex(i)[2:] for i in cip])
    
    
KEY = [randbelow(16) for _ in range(16)]

OTP = b""
while len(OTP) < len(FLAG):
    OTP += sha256(b" :: ".join([b"OTP", str(KEY).encode(), len(OTP).to_bytes(2, 'big')])).digest()
    
encflag = bytes([i ^ j for i,j in zip(FLAG, OTP)]).hex()

print("|\n|  ~ In order to prove that I have nothing up my sleeve, I let you decide on the sbox!")
print("|    I am so confident, I will even stake my flag on it ::")
print("|    flag = {}".format(encflag))

print("|\n|  ~ Now, player, what should I call you?")
seed = input("|\n|  > ")

oracle = NUMSBOX(seed, KEY)

print("|\n|  ~ Well {}, here are your s- and p-box ::".format(seed))
print("|    s-box = {}".format(oracle.sbox))
print("|    p-box = {}".format(oracle.pbox))


MENU = """|
|  ~ Menu ::
|    [E]ncrypt
|    [Q]uit
|"""

while True:

    try:

        print(MENU)
        choice = input("|  > ")

        if choice.lower() == 'e':
            msg = [int(i, 16) for i in input("|\n|  > (hex) ")]
            print("|\n|  ~ {}".format(oracle.encrypt(msg)))

        elif choice.lower() == 'q':
            print("|\n|  ~ Sweeping the boxes back up my sleeve...\n|")
            break

        else:
            print("|\n|  ~ Sorry I do not know what you mean...")

    except KeyboardInterrupt:
        print("\n|  ~ Sweeping the boxes back up my sleeve...\n|")
        break

    except:
        print("|\n|  ~ Hey, be nice to my code, okay?")
