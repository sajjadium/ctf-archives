import random
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes

"""
Key-scheduling algorithm (KSA)
"""
def KSA(key):
    S = [i for i in range(0, 256)]
    i = 0
    for j in range(0, 256):
        i = (i + S[j] + key[j % len(key)]) % 256
        
        S[i] ^= S[j] ## swap values of S[i] and S[j]
        S[j] ^= S[i]
        S[i] ^= S[j]
        
    return S
    
"""
Pseudo-random generation algorithm (PRGA)
"""
def PGRA(S):
    i = 0
    j = 0
    while True: ## while GeneratingOutput
        i = (1 + i) % 256
        j = (S[i] + j) % 256
        
        S[i] ^= S[j] ## swap values of S[i] and S[j]
        S[j] ^= S[i]
        S[i] ^= S[j]
        
        yield S[(S[i] + S[j]) % 256]        

    

if __name__ == '__main__':
    FLAG = 'bctf{REDACTED}'
    print("Would you like to pad the plaintext before encrypting it?")
    print("(Just hit enter if you do not want to add any padding(s).)")
    Padding = input()
    input_text = ''
    input_text += Padding
    input_text += FLAG

    plaintext = [ord(char) for char in input_text]
    key = long_to_bytes(random.getrandbits(2048)) # 2048 bits = 256 bytes
    key = [byte for byte in key]

    S = KSA(key)
    keystream = PGRA(S)
    
    ciphertext = ''
    for char in plaintext:
        enc = char ^ next(keystream)
        enc = (str(hex(enc)))[2:]
        if len(enc) == 1: ## make sure they are all in the form 0x**
            enc = '0' + enc
        ciphertext += enc

    print(ciphertext)