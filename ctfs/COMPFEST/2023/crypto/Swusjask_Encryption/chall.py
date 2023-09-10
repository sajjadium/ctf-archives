from Crypto.Util.number import long_to_bytes, bytes_to_long

p = 1179478847235411356076287763101027881
e = 0x10001


def bytes_to_block(msg: bytes):
    res = []
    msg_int = bytes_to_long(msg)
    while msg_int:
        res.append(msg_int % (p**2))
        msg_int //= p**2
    return res


def block_to_bytes(blocks: list[int]):
    res = 0
    for i in range(len(blocks) - 1, -1, -1):
        res *= p**2
        res += blocks[i]
    return long_to_bytes(res)


class MultiplicativeGroup:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __mul__(self, other) -> "MultiplicativeGroup":
        a = (self.a * other.a - 6969 * self.b * other.b) % p
        b = (self.a * other.b + self.b * other.a - 69 * self.b * other.b) % p
        return MultiplicativeGroup(a, b)

    def __pow__(self, n) -> "MultiplicativeGroup":
        res = MultiplicativeGroup(1, 0)
        base = self
        while n:
            if n & 1:
                res *= base
            base *= base
            n >>= 1
        return res
    
    def __repr__(self):
        return f"({self.a}, {self.b})"


if __name__ == "__main__":
    FLAG = open("flag.png", "rb").read()
    blocks = bytes_to_block(FLAG)
    enc = []
    for block in blocks:
        assert block < p**2
        a = block % p
        b = block // p
        m = MultiplicativeGroup(a, b)
        c = m ** e
        enc.append(c.a + c.b * p)
        
    open("flag.enc", "wb").write(block_to_bytes(enc))