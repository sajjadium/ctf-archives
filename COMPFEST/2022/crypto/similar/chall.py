from Crypto.Cipher import AES
from Crypto.Util import Padding, number
from secret import flag, seed
import hashlib, secrets

class LFSR:
    def __init__(self, state, taps):
        self.state = state
        self.taps = [len(state) - t for t in taps]

    def clock(self):
        out = self.state[0]
        self.state = self.state[1:] + [sum(self.state[t] for t in self.taps)%2]
        return out

class Generator:
    def __init__(self, seed):
        self.seed = list(map(int, bin(seed)[2:]))
        assert len(self.seed) == 99
        self.lfsr = [LFSR(self.seed[:37], [37, 5, 4, 3, 2, 1]), 
                     LFSR(self.seed[37:56], [19, 6, 2, 1]), 
                     LFSR(self.seed[56:80], [24, 23, 22, 17]), 
                     LFSR(self.seed[80:], [19, 6, 2, 1])]
    
    def combined_clock(self):
        bits = [l.clock() for l in self.lfsr]
        return bits[0] if bits[1] else bits[2] if bits[3] else bits[0]

def encrypt(ptxt, key):
    key = hashlib.sha256(number.long_to_bytes(key)).digest()[:16]
    iv = secrets.token_bytes(16)
    cipher = AES.new(key, 2, iv)
    ctxt = cipher.encrypt(Padding.pad(ptxt, 16))
    return (iv + ctxt).hex()

G = Generator(seed)
stream = [G.combined_clock() for _ in range(256)]
ctxt = encrypt(flag, seed)

with open('out.txt', 'w') as f:
    print(stream, file=f)
    print(ctxt, file=f)