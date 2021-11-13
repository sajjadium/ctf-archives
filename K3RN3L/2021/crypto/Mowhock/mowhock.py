#!/usr/bin/env python3
#
# Nika Soltas
#

# Imports
import os
from hashlib import sha256

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

class Map:
    def __init__(self, maptype, params):
        """Initialise map object"""
        if maptype.lower() in ['l','lm','logic']:
            self.f = self.__LOGI
        elif maptype.lower() in ['e','el','elm','extended logic']:
            self.f = self.__EXT_LOGI
        else:
            raise ValueError('Invalid Map Type.')
        try:
            self.p = list(params)
        except:
            self.p = [params]
            
    def __LOGI(self, x):       # <--- p in [3.7, 4]
        """Logistic map"""
        return self.p[0] * x * (1 - x)
    
    def __EXT_LOGI(self, x):   # <--- p in [2, 4]
        """Extended logistic map"""
        if x < 0.5:
            return self.__LOGI(x)
        else:
            return self.p[0] * (x * (x - 1) + 1 / 4)
    
    def sample(self, x_i, settles, samples):
        """Generates outputs after certain number of settles"""
        x = x_i
        for _ in range(settles):
            x = self.f(x)
        ret = []
        for _ in range(samples):
            x = self.f(x)
            ret += [x]
        return ret


class Mowhock:
    def __init__(self, key=None, iv=None):
        """Initialise Mowhock class object."""
        if (key is None) or (len(key) != 64):
            key = os.urandom(32).hex()
        self.key = key
        if (iv is None) or (len(iv) != 16):
            iv = os.urandom(8).hex()
        self.iv = iv
        self.maps = self.map_schedule()
        self.buffer_raw = None
        self.buffer_byt = None
        
    def key_schedule(self):
        """Convert key into 8 round subkeys."""
        KL, KR = self.key[:32], self.key[32:]
        VL, VR = self.ctr[:8], self.ctr[8:]
        HL, HR = [sha256(bytes.fromhex(i)).digest() for i in [VL+KL,VR+KL]]
        hlbits, hrbits = ['{:0256b}'.format(int.from_bytes(H,'big')) for H in [HL,HR]]
        bitweave = ''.join([hlbits[i]+hrbits[i] for i in range(256)])
        subkeys = [int(bitweave[i:i+64],2) for i in range(0,512,64)]
        return [self.read_subkey(i) for i in subkeys]

    def map_schedule(self):
        """Convert IV into 8 maps with iv-dependent parameters"""
        iv = bytes.fromhex(self.iv)
        maps = [
            Map('L', iv[0]*(4.00 - 3.86)/255 + 3.86),
            Map('L', iv[1]*(4.00 - 3.86)/255 + 3.86),
            Map('L', iv[2]*(4.00 - 3.86)/255 + 3.86),
            Map('L', iv[3]*(4.00 - 3.86)/255 + 3.86),
            Map('E', iv[4]*(4.00 - 3.55)/255 + 3.55),
            Map('E', iv[5]*(4.00 - 3.55)/255 + 3.55),
            Map('E', iv[6]*(4.00 - 3.55)/255 + 3.55),
            Map('E', iv[7]*(4.00 - 3.55)/255 + 3.55),
        ]
        order = self.hop_order(int(self.key[:2],16),8)
        return [maps[i] for i in order]

    def read_subkey(self, subkey):
        """Convert subkey int from key schedule to orbit parameters."""
        # Integer to bits
        byts = subkey.to_bytes(8, 'big')
        bits = ''.join(['{:08b}'.format(i) for i in byts])
        # Read key elements
        hpsn    = int(bits[0:8],2)
        seed    = float('0.00'+str(int(bits[8:32],2)))
        offset  = float('0.0000'+str(int(bits[32:48],2)))
        settles = int(bits[48:56],2) + 512
        orbits  = int(bits[56:60],2) + 4
        samples = int(bits[60:64],2) + 4
        # Processing key elements
        hopord  = self.hop_order(hpsn,orbits)
        x_i     = [seed + offset*i for i in hopord]
        # Return subkey dictionary
        return {
            'order'    : hopord,
            'hpsn'     : hpsn,
            'seed'     : seed,
            'offset'   : offset,
            'x_i'      : x_i,
            'settles'  : settles,
            'orbits'   : orbits,
            'samples'  : samples
        }

    def hop_order(self, hpsn, orbits):
        """Determine orbit hop order"""
        i = 1
        ret = []
        while len(ret) < orbits:
            o = (pow(hpsn,i,256)+i) % orbits
            if o not in ret:
                ret += [o]
            i += 1
        return ret
    
    def ctr_increment(self):
        """Increments IV and reschedules key."""
        self.ctr = (int(self.ctr,16) + 1).to_bytes(8, 'big').hex()
        self.subkeys = self.key_schedule()
        self.fill_buffers()
        
    def fill_buffers(self, save_raw=False):
        """Fills internal buffer with pseudorandom bytes"""
        self.buffer_raw = []
        self.buffer_byt = []
        raw = []
        for i in range(8):
            settles = self.subkeys[i]['settles']
            samples = self.subkeys[i]['samples']
            for x_i in self.subkeys[i]['x_i']:
                raw += self.maps[i].sample(x_i, settles, samples)
        if save_raw:
            self.buffer_raw += raw
        bitstr = ['{:032b}'.format(int(i*2**53)) for i in raw]
        byt = []
        for b32 in bitstr:
            byt += [int(b32[:8],2) ^ int(b32[16:24],2), int(b32[8:16],2) ^ int(b32[24:32],2)]
        self.buffer_byt += bytes(byt)

    def encrypt(self, msg):
        """Encrypts a message through the power of chaos"""
        # Fill initial buffers
        self.ctr = self.iv
        self.subkeys = self.key_schedule()
        self.fill_buffers()
        # Encrypt (increment and refill buffers if necessary)
        cip = b''
        if type(msg) == str:
            msg = bytes.fromhex(msg)
        for byt in msg:
            try:
                cip += bytes( [byt ^ self.buffer_byt.pop(0)] )
            except:
                self.ctr_increment()
                cip += bytes( [byt ^ self.buffer_byt.pop(0)] )
        # Return IV and ciphertext
        return self.iv + cip.hex()

#-----------------------------------------------------------------------------------------------------
# CHALLENGE
#-----------------------------------------------------------------------------------------------------
HDR = r"""|
|    __    __     _____     _      _   __   __    _____     _____   __  __   
|   /_/\  /\_\   ) ___ (   /_/\  /\_\ /\_\ /_/\  ) ___ (   /\ __/\ /\_\\  /\ 
|   ) ) \/ ( (  / /\_/\ \  ) ) )( ( (( ( (_) ) )/ /\_/\ \  ) )__\/( ( (/ / / 
|  /_/ \  / \_\/ /_/ (_\ \/_/ //\\ \_\\ \___/ // /_) \_\ \/ / /    \ \_ / /  
|  \ \ \\// / /\ \ )_/ / /\ \ /  \ / // / _ \ \\ \ \_( / /\ \ \_   / /  \ \  
|   )_) )( (_(  \ \/_\/ /  )_) /\ (_(( (_( )_) )\ \/_\/ /  ) )__/\( (_(\ \ \ 
|   \_\/  \/_/   )_____(   \_\/  \/_/ \/_/ \_\/  )_____(   \/___\/ \/_//__\/ 
|                                                                            
|                   ENCRYPTION through the POWER of CHAOS
|"""

MEN = r"""|
|
|  Menu:
|   [1] Encrypt custom message
|   [2] Encrypt FLAG
|"""

print(HDR)

used_ivs = []

while True:

    try:

        print(MEN)
        choice = input("|   >> ")

        if choice == "1":
            
            print("|\n|\n|  Custom encryption parameters (HEX) [empty for RANDOM]:")
            key = input("|   Key: ")
            iv  = input("|   IV : ")
            msg = input("|   Msg: ")

            try:
                bytes.fromhex(key); bytes.fromhex(iv); bytes.fromhex(msg)
                assert len(key) in [0,64] and len(iv) in [0,16]
            except:
                print('|\n|  ERROR -- Invalid user input.')
                continue

            while True:
                cip = Mowhock(key=key,iv=iv).encrypt(msg)

                used_iv = cip[:16]
                if used_iv not in used_ivs:
                    used_ivs += [used_iv]
                    break

            print("|\n|  Output:")
            print("|   {}".format(cip))

        elif choice == "2":

            print("|\n|\n|  FLAG encryption parameters (HEX) [empty for RANDOM]:")
            print("|   Key: <RANDOM>")
            iv = input("|   IV : ")
            print("|   Msg: <RANDOM>|<FLAG>|<RANDOM>")

            try:
                bytes.fromhex(iv)
                assert len(iv) in [0,16]
            except:
                print('|\n|  ERROR -- Invalid user input.')
                continue

            rnum = [int(i,16) for i in list(os.urandom(1).hex())]
            cip = Mowhock(key=None,iv=iv).encrypt(os.urandom(rnum[0])+FLAG+os.urandom(rnum[1]))

            if cip[:16] in used_ivs:
                print('|\n|  ERROR -- IV re-use detected.')
                continue

            used_ivs += [cip[:16]]

            print("|\n|  Output:")
            print("|   {}".format(cip))

    except KeyboardInterrupt:
        print("\n|\n|  May your day be CHAOTIC!\n|")
        exit(0)

    except:
        print("|\n|\n|  ERROR --- TOO MUCH CHAOS ---\n|")
