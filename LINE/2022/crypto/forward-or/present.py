'''
Python3 PRESENT implementation

original code (implementation for python2) is here:
http://www.lightweightcrypto.org/downloads/implementations/pypresent.py
'''


'''
key = bytes.fromhex("00000000000000000000")
plain = bytes.fromhex("0000000000000000")
cipher = Present(key)
encrypted = cipher.encrypt(plain)
print(encrypted.hex())
>> '5579c1387b228445'
decrypted = cipher.decrypt(encrypted)
decrypted.hex()
>> '0000000000000000'
'''

class Present:

    def __init__(self,key,rounds=32):
        """Create a PRESENT cipher object

        key:    the key as a 128-bit or 80-bit rawstring
        rounds: the number of rounds as an integer, 32 by default
        """
        self.rounds = rounds
        if len(key) * 8 == 80:
            self.roundkeys = generateRoundkeys80(byte2number(key),self.rounds)
        elif len(key) * 8 == 128:
            self.roundkeys = generateRoundkeys128(byte2number(key),self.rounds)
        else:
            raise (ValueError, "Key must be a 128-bit or 80-bit rawstring")

    def encrypt(self,block):
        """Encrypt 1 block (8 bytes)

        Input:  plaintext block as raw string
        Output: ciphertext block as raw string
        """
        state = byte2number(block)
        for i in range(self.rounds-1):
            state = addRoundKey(state,self.roundkeys[i])
            state = sBoxLayer(state)
            state = pLayer(state)
        cipher = addRoundKey(state,self.roundkeys[-1])
        return number2byte_N(cipher,8)

    def decrypt(self,block):
        """Decrypt 1 block (8 bytes)

        Input:  ciphertext block as raw string
        Output: plaintext block as raw string
        """
        state = byte2number(block)
        for i in range(self.rounds-1):
            state = addRoundKey(state,self.roundkeys[-i-1])
            state = pLayer_dec(state)
            state = sBoxLayer_dec(state)
        decipher = addRoundKey(state,self.roundkeys[0])
        return number2byte_N(decipher,8)

    def get_block_size(self):
        return 8

#    0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
Sbox= [0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2]
Sbox_inv = [Sbox.index(x) for x in range(16)]
PBox = [0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,
    4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,
    8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,
    12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
PBox_inv = [PBox.index(x) for x in range(64)]

def generateRoundkeys80(key,rounds):
    """Generate the roundkeys for a 80-bit key

    Input:
        key:    the key as a 80-bit integer
        rounds: the number of rounds as an integer
    Output: list of 64-bit roundkeys as integers"""
    roundkeys = []
    for i in range(1,rounds+1): # (K1 ... K32)
        # rawkey: used in comments to show what happens at bitlevel
        # rawKey[0:64]
        roundkeys.append(key >>16)
        #1. Shift
        #rawKey[19:len(rawKey)]+rawKey[0:19]
        key = ((key & (2**19-1)) << 61) + (key >> 19)
        #2. SBox
        #rawKey[76:80] = S(rawKey[76:80])
        key = (Sbox[key >> 76] << 76)+(key & (2**76-1))
        #3. Salt
        #rawKey[15:20] ^ i
        key ^= i << 15
    return roundkeys

def generateRoundkeys128(key,rounds):
    """Generate the roundkeys for a 128-bit key

    Input:
        key:    the key as a 128-bit integer
        rounds: the number of rounds as an integer
    Output: list of 64-bit roundkeys as integers"""
    roundkeys = []
    for i in range(1,rounds+1): # (K1 ... K32)
        # rawkey: used in comments to show what happens at bitlevel
        roundkeys.append(key >>64)
        #1. Shift
        key = ((key & (2**67-1)) << 61) + (key >> 67)
        #2. SBox
        key = (Sbox[key >> 124] << 124)+(Sbox[(key >> 120) & 0xF] << 120)+(key & (2**120-1))
        #3. Salt
        #rawKey[62:67] ^ i
        key ^= i << 62
    return roundkeys

def addRoundKey(state,roundkey):
    return state ^ roundkey

def sBoxLayer(state):
    """SBox function for encryption

    Input:  64-bit integer
    Output: 64-bit integer"""

    output = 0
    for i in range(16):
        output += Sbox[( state >> (i*4)) & 0xF] << (i*4)
    return output

def sBoxLayer_dec(state):
    """Inverse SBox function for decryption

    Input:  64-bit integer
    Output: 64-bit integer"""
    output = 0
    for i in range(16):
        output += Sbox_inv[( state >> (i*4)) & 0xF] << (i*4)
    return output

def pLayer(state):
    """Permutation layer for encryption

    Input:  64-bit integer
    Output: 64-bit integer"""
    output = 0
    for i in range(64):
        output += ((state >> i) & 0x01) << PBox[i]
    return output

def pLayer_dec(state):
    """Permutation layer for decryption

    Input:  64-bit integer
    Output: 64-bit integer"""
    output = 0
    for i in range(64):
        output += ((state >> i) & 0x01) << PBox_inv[i]
    return output

def byte2number(i):
    """ Convert a string to a number

    Input: byte (big-endian)
    Output: long or integer
    """
    return int.from_bytes(i, 'big')

def number2byte_N(i, N):
    """Convert a number to a string of fixed size

    i: long or integer
    N: length of byte
    Output: string (big-endian)
    """
    return i.to_bytes(N, byteorder='big')

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()