from Crypto.Util.number import bytes_to_long as b2l

FLAG = open('flag.txt', 'r').read().strip().encode()

class LFSR():
    def __init__(self, iv):
        self.state = [int(c) for c in iv]
        #self.state = self.iv

    def shift(self):
        s = self.state
        newbit = s[15] ^ s[13] ^ s[12] ^ s[10] # ^ s[0]
        s.pop()
        self.state = [newbit] + s

for i in range(0, len(FLAG), 2):
    chars = f'{b2l(FLAG[i:i+2]):016b}'
    assert len(chars) == 16

    lfsr = LFSR(chars)
    for _ in range(31337):
        lfsr.shift()

    finalstate = ''.join([str(c) for c in lfsr.state])
    print(f'{finalstate}')


