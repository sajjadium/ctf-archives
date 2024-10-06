import random
def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

class CustomRandom:
    def __init__(self, m, a=None, b=None, x=None) -> None:
        if a is None:
            self.a = random.getrandbits(64)
            self.b = random.getrandbits(64)
            self.x = random.getrandbits(64)
        else:
            self.a = a
            self.b = b
            self.x = x

        self.m = m
        print(f"{self.x = }")

    def next_bytes(self):
        self.x = (self.a*self.x + self.b) % self.m
        return int(bin(self.x)[-16:-9],2),int(bin(self.x)[-23:-16],2)


r = CustomRandom(2**64)

im = open("flag.png", 'rb').read()
ks = [x for _ in range(len(im)//2 + 1) for x in r.next_bytes()]
ct = xor(im, ks)
f = open('flag.enc','wb')
f.write(ct)
f.close()

# self.x = 9014855307380235246