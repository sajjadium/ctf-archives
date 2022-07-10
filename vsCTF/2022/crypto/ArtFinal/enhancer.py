# Teacher, please give me an A
import random
from PIL import Image


boring = Image.open('Art_Final_2022.png', 'r').convert('RGBA')
boring_pix = boring.load()

spicy = Image.new('RGBA', boring.size)
spicy_pix = spicy.load()

# Add SPICE
for i in range(boring.size[0] * boring.size[1]):
    x = i % boring.size[0]
    y = i // boring.size[0]
    rgba = tuple(random.randbytes(4))
    spicy_pix[x, y] = tuple([bore ^ spice for bore, spice in zip(boring_pix[x, y], rgba)])

# This final is HOT
spicy.save('ENHANCED_Final_2022.png')


# oh shoot, i forgot there needs to be a flag ._.
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode

key = bytes(random.sample(random.randbytes(16), 16))
iv = Random.new().read(AES.block_size)
enc = AES.new(key, AES.MODE_CBC, iv)
flag = b64encode(iv + enc.encrypt(pad(b'[REDACTED]', AES.block_size))).decode()

print(flag)  # Tl5nK8L2KYZRCJCqLF7TbgKLgy1vIkH+KIAJv5/ILFoC+llemcmoLmCQYkiOrJ/orOOV+lwX+cVh+pwE5mtx6w==
