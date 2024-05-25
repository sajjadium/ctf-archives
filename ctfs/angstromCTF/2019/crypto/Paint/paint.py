import binascii
import random

from secret import flag

image = int(binascii.hexlify(flag), 16)

palette = 1 << 2048
base = random.randint(0, palette) | 1
secret = random.randint(0, palette)
my_mix = pow(base, secret, palette)

print('palette: {}'.format(palette))
print('base: {}'.format(base))
print('my mix: {}'.format(my_mix))

your_mix = int(input('your mix: '))

shared_mix = pow(your_mix, secret, palette)
painting = image ^ shared_mix
print('painting: {}'.format(painting))