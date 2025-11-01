import secrets
FLAG = b"n1ctf{REDACTED}"

Ns = [14, 32, 24, 48, 8, 8, 8, 8, 10]
MASKS = [0x7a7, 0xcfdf1bcf, 0xb9ca5b, 0x83c7efefc783, 0x27, 0x65, 0x63, 0x2b, 0x243]
Filters = [
    237861018962211057901759878514586912107,
    69474900172976843852504521249820447513188207961992185137442753975916133181030,
    28448620439946980695145546319125628439828158154718599921182092785732019632576,
    16097126481514198260930631821805544393127389525416543962503447728744965087216,
    7283664602255916497455724627182983825601943018950061893835110648753003906240,
    55629484047984633706625341811769132818865100775829362141410613259552042519543,
    4239659866847353140850509664106411172999885587987448627237497059999417835603,
    85329496204666590697103243138676879057056393527749323760467772833635713704461
]

extract = lambda x,b: sum(((x >> p) & 1) << i for i, p in enumerate(b))
blur = lambda x,i: (Filters[i] >> x) & 1

class LFSR:
    def __init__(self, n, key, mask):
        self.n = n
        self.state = key & ((1 << n) - 1)
        self.mask = mask

    def __call__(self):
        b = self.state & 1
        self.state = (self.state >> 1) | (
            ((self.state & self.mask).bit_count() & 1) << (self.n - 1)
        )
        return b

class Cipher:
    def __init__(self, key):
        self.lfsrs = []
        for i in range(len(Ns)):
            self.lfsrs.append(LFSR(Ns[i], key, MASKS[i]))
            key >>= Ns[i]

    def bit(self):
        x = blur(extract(self.lfsrs[0].state, [5, 9, 1, 0, 4, 11, 13]), 0)
        y = self.lfsrs[1].state & 1
        z = blur(extract(self.lfsrs[2].state, [20, 2, 16, 11, 1, 23, 22, 8]), 1)
        w = blur(extract(self.lfsrs[3].state, [1, 46, 21, 7, 43, 0, 27, 39]), 2)
        v = blur(extract(self.lfsrs[4].state, [1, 3, 7, 4, 5, 0, 6, 2]), 3)
        u = blur(self.lfsrs[5].state, 4) ^ blur(self.lfsrs[6].state, 5) ^ blur(self.lfsrs[7].state, 6)
        t = blur(extract(self.lfsrs[8].state, [5, 8, 9, 3, 1, 0, 2, 4]), 7)
        for lfsr in self.lfsrs: lfsr()
        return x ^ y ^ z ^ w ^ v ^ u ^ t

    def stream(self):
        while True:
            b = 0
            for i in reversed(range(8)):
                b |= self.bit() << i
            yield b

    def encrypt(self, pt: bytes):
        return bytes([x ^ y for x, y in zip(pt, self.stream())])

key = secrets.randbits(160)
cipher = Cipher(key)
tk = secrets.token_bytes(15)
__import__("signal").alarm(5)
print("ct:", cipher.encrypt(b"\x00"*80+tk).hex())
if input("Gimme Token: ") == tk.hex():
    print("Here is your flag:", FLAG)