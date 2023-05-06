from secrets import randbits
from random import shuffle
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class LFSR:
    def __init__(self, key, taps):
        self.key = key
        self.taps = taps
        self.state = list(map(int, list("{:0128b}".format(key))))
    
    def _clock(self):
        ob = self.state[0]
        self.state = self.state[1:] + [sum([self.state[t] for t in self.taps]) % 2]
        return ob

key = randbits(128)
l = LFSR(key, [1, 2, 7, 3, 12, 73])
out = []

for i in range(118):
    bits = [l._clock() for _ in range(128)]
    shuffle(bits)
    out += bits

print(hex(sum([bit*2**i for i, bit in enumerate(out)])))

flag = open("flag.txt", "rb").read()
iv = randbits(128).to_bytes(16, 'big')
aeskey = sha256(key.to_bytes(16, 'big')).digest()[:32]
print((iv + AES.new(aeskey, AES.MODE_CBC, iv=iv).encrypt(pad(flag, 16))).hex())