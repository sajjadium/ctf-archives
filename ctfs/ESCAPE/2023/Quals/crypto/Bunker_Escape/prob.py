from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from gmpy2 import invert

class Cipher:
    def __init__(self):
        self.n = 108506951736793336490683880256855846248083684741694466461336182348417411176781023957825388818844036495751633876599810798436954790114984279939172259886462851438954959031979074506295441495658302003723943179142742062326225122087241430684094279948641138924448463919864585525265270367948313098530841624367001646231
        self.e = 65537

    def encrypt(self, msg):
        return pow(msg, self.e, self.n)

ments = [
    ?, ?, ?, ?, ?, ...
        ]

RSA = Cipher()

while True:
    for ment in ments:
        c = RSA.encrypt(bytes_to_long(ment))
        print(c)
