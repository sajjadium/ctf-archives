load("ehasher.sage")
load("chasher.sage")
assert "EHasherHellman" in globals()
assert "EHasherRemy" in globals()
assert "CHasherLorenz" in globals()
assert "CHasherPanny" in globals()

class Protocol:
    def __init__(self, flag):
        self.ehasherorz = EHasherHellman
        self.ehashercat = EHasherRemy
        self.chashery = CHasherLorenz
        self.chasherx7 = CHasherPanny
        # Typo
        self.flag = flag

    # yx7 + hellman = yellman
    def yellman(self):
        return (self.ehasherorz, self.chashery)

    # remy + yx7 = remx7
    def remx7(self):
        return (self.ehashercat, self.chasherx7)

    # multiple orz's = mystizes
    def mystizes(self):
        return [self.yellman(), self.remx7()]

    def airine(self, hasher):
        _, chasher = hasher
        ubound = product(chasher.l)**(2**(80 // chasher.n))
        return 3**(floor(ubound.log(3) * 3 / 8))

    def vemtre(self, hasher, h, forgor):
        _, chasher = hasher
        if forgor < chasher.n:
            hs = input("I forgor hs: ").strip()
            hs = list(map(ZZ, hs.split(",")))
        else:
            hs = ZZ(h % 2**(80 // chasher.n * chasher.n)).digits(2**(80 // chasher.n), padto=chasher.n)
        assert len(hs) == chasher.n
        c, d = chasher.lepsuk(0, hs, forgor=forgor)
        return h, c, d % self.airine(hasher)

    def kaspar(self, hasher, msg, forgor):
        ehasher, _ = hasher
        h = ehasher.kuspel(msg % ehasher.p)
        return self.vemtre(hasher, h, forgor=forgor)

    def matsub(self, msg, forgores=[80, 20]):
        sig = []
        for forgor, hasher in zip(forgores, self.mystizes()):
            sig.append(self.kaspar(hasher, msg, forgor=forgor))
        return tuple(sig)

    def challenge(self):
        msg = os.urandom(10)
        msg_r = int.from_bytes(msg, "big")
        sigma = self.matsub(msg_r)
        print("sigma male:", sigma)

        print("Are you as good as Mystiz?")
        # Mystiz is too old. He forgor.
        msg1 = bytes.fromhex(input("andrew tate? ").strip()[:10])
        msg1_r = int.from_bytes(msg1, "big")
        neobeo = self.matsub(msg1_r, forgores=[45, 2])

        msg2 = bytes.fromhex(input("john tate? ").strip()[:10])
        msg2_r = int.from_bytes(msg2, "big")
        имя_пользователя = self.matsub(msg2_r, forgores=[45, 2])
        return msg1 != msg2 and neobeo == имя_пользователя == sigma

    # Corrected
    def falg(self):
        return self.flag


if __name__ == "__main__":
    import os
    FLAG = os.environ.get("FLAG", "b6actf{owo}")
    Server = Protocol(FLAG)
    for _ in range(5):
        assert Server.challenge()
    print("Falg:", Server.falg())
