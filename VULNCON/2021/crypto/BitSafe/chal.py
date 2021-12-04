from Crypto.Util.number import getRandomRange, long_to_bytes, bytes_to_long, inverse, GCD


class BitSafe:
    def __init__(self, msg):
        self.mbits = bin(bytes_to_long(msg))[2:]
        self.tbits = len(self.mbits)

    def keygen(self):
        self.pub = []
        self.priv = [ getRandomRange(2, 1 << 10) ]
        s = self.priv[0]

        for i in range(1, self.tbits):
            self.priv.append( getRandomRange(s+1, s << 5) )
            s += self.priv[i]

        self.q = getRandomRange(s+1, s << 5)
        
        while True:
            self.r = getRandomRange(2, self.q)
            if GCD(self.r, self.q) == 1:
                break

        self.pub = [ self.r * w_i % self.q for w_i in self.priv ]

    def encrypt(self):
        cipher = 0
        for i, bit in enumerate(self.mbits):
            cipher += int(bit) * self.pub[i]
        return hex(cipher)[2:]

    def decrypt(self, cipher):
        rp = inverse(self.r, self.q)
        cp = int(cipher, 16) * rp % self.q
        mbits = ''
        for w_i in reversed(self.priv):
            if cp - w_i >= 0:
                mbits = '1' + mbits
                cp -= w_i
            else:
                mbits = '0' + mbits
        msg = long_to_bytes(int(mbits, 2))
        return msg


if __name__ == '__main__':
    
    FLAG = open('flag.txt', 'rb').read().strip()

    safe = BitSafe(FLAG)
    safe.keygen()

    cipher = safe.encrypt()
    
    assert safe.decrypt(cipher) == FLAG, "Something's Wrong !!!"
    
    with open('output.py', 'w') as f:
        f.write('pub = %s\n' % str(safe.pub))
        f.write('cipher = 0x%s' % str(cipher))

    print("Your Secret is Safe with us !!!")
