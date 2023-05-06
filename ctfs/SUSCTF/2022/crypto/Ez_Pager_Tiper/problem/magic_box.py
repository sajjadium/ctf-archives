class lfsr():
    def __init__(self, seed, mask, length):
        self.length_mask = 2 ** length - 1
        self.mask = mask & self.length_mask
        self.state = seed & self.length_mask

    def next(self):
        next_state = (self.state << 1) & self.length_mask
        i = self.state & self.mask & self.length_mask
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        next_state ^= output
        self.state = next_state
        return output

    def getrandbit(self, nbit):
        output = 0
        for _ in range(nbit):
            output = (output << 1) ^ self.next()
        return output


class generator():
    def __init__(self, lfsr1, lfsr2, magic):
        self.lfsr1 = lfsr1
        self.lfsr2 = lfsr2
        self.magic = magic

    def infinit_power(self, magic):
        return int(magic)

    def malicious_magic(self, magic):
        now = (-magic & magic)
        magic ^= now
        return int(now), int(magic)

    def confusion(self, c1, c2):
        magic = self.magic
        output, cnt = magic, 0
        output ^= c1 ^ c2
        while magic:
            now, magic = self.malicious_magic(magic)
            cnt ^= now >> (now.bit_length() - 1)
            output ^= now
        output ^= cnt * c1
        return int(output)

    def getrandbit(self, nbit):
        output1 = self.lfsr1.getrandbit(nbit)
        output2 = self.lfsr2.getrandbit(nbit)
        return self.confusion(output1, output2)