from Crypto.Util.number import inverse
from hashlib import sha256
import os
import signal

class NonceGenerator:
    def __init__(self):
        self.state = os.urandom(10)
        self.db = {}
    
    def gen(self):
        self.state = sha256(self.state + b'wow').digest()[:10]
        key = sha256(self.state).digest()[:8]
        self.db[key] = self.state

        return int.from_bytes(self.state, 'big'), key

    def get(self, key: str):
        if key not in self.db:
            print("Wrong key :(")
            exit(0)

        return int.from_bytes(self.db[key], 'big')


class ECPoint:
    def __init__(self, point, mod):
        self.x = point[0]
        self.y = point[1]
        self.mod = mod

    def inf(self):
        return ECPoint((0, 0), self.mod)

    def _is_inf(self):
        return self.x == 0 and self.y == 0

    def __eq__(self, other):
        assert self.mod == other.mod
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        assert self.mod == other.mod
        P, Q = self, other
        if P._is_inf() and Q._is_inf():
            return self.inf()
        elif P._is_inf():
            return Q
        elif Q._is_inf():
            return P

        if P == Q:
            lam = (3 * P.x**2 - 3) * inverse(2 * P.y, self.mod) % self.mod
        elif P.x == Q.x:
            return self.inf()
        else:
            lam = (Q.y - P.y) * inverse(Q.x - P.x, self.mod) % self.mod

        x = (lam**2 - P.x - Q.x) % self.mod
        y = (lam * (P.x - x) - P.y) % self.mod

        return ECPoint((x, y), self.mod)

    def __rmul__(self, other: int):
        base, ret = self, self.inf()
        while other > 0:
            if other & 1:
                ret = ret + base
            other >>= 1
            base = base + base
        return ret


class MyECCService:
    BASE_POINT = (2, 3)
    MODS = [
        942340315817634793955564145941,
        743407728032531787171577862237,
        738544131228408810877899501401,
        1259364878519558726929217176601,
        1008010020840510185943345843979,
        1091751292145929362278703826843,
        793740294757729426365912710779,
        1150777367270126864511515229247,
        763179896322263629934390422709,
        636578605918784948191113787037,
        1026431693628541431558922383259,
        1017462942498845298161486906117,
        734931478529974629373494426499,
        934230128883556339260430101091,
        960517171253207745834255748181,
        746815232752302425332893938923,
    ]

    def __init__(self):
        self.nonce_gen = NonceGenerator()

    def get_x(self, nonce: int) -> bytes:
        ret = b""
        for mod in self.MODS:
            p = ECPoint(self.BASE_POINT, mod)
            x = (nonce * p).x
            ret += x.to_bytes(13, "big")
        return ret

    def gen(self) -> bytes:
        nonce, key = self.nonce_gen.gen()
        x = self.get_x(nonce)

        return b"\x02\x03" + key + x

    def verify(self, inp: bytes) -> bool:
        assert len(inp) == 218

        nonce = self.nonce_gen.get(inp[2:10])
        self.BASE_POINT = (inp[0], inp[1])
        x = self.get_x(nonce)
        return inp[10:] == x


def handler(_signum, _frame):
    print("Time out!")
    exit(0)


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    service = MyECCService()

    for _ in range(100):
        service.gen()

    while True:
        inp = input("> ")
        if inp == "G":
            payload = service.gen()
            print(f"Payload: {payload.hex()}")
        elif inp == "V":
            payload = bytes.fromhex(input("Payload: "))
            result = service.verify(payload)
            print(f"Result: {result}")
        elif inp == "P":
            payload = bytes.fromhex(input("Payload: "))
            answer = service.gen()

            if payload == answer:
                with open("flag.txt", "r") as f:
                    print(f.read())
            else:
                print("Wrong :(")
            exit(0)


if __name__ == "__main__":
    main()
