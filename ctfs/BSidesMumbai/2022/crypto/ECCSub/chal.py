import os

FLAG = open('flag.txt', 'rb').read().strip()


def ECC_encode(x):
    y2 = (x**3 + a*x + b) % p
    return y2

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

C = [ hex(ECC_encode(int(os.urandom(8).hex() + hex(k)[2:], 16))) for k in FLAG ]

open('flag.enc', 'w').write(str(C))
