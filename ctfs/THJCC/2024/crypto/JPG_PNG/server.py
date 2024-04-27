from itertools import cycle

def xor(a, b):
    return [i^j for i, j in zip(a, cycle(b))]

KEY= open("key.png", "rb").read()
FLAG = open("flag.jpg", "rb").read()

key=[KEY[0], KEY[1], KEY[2], KEY[3], KEY[4], KEY[5], KEY[6], KEY[7]]

enc = bytearray(xor(FLAG,key))

open('enc.txt', 'wb').write(enc)
