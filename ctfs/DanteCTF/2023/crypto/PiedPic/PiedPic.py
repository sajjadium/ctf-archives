#!/usr/bin/env python3

from PIL import Image
from Crypto.Random import get_random_bytes
from io import BytesIO
from base64 import b64encode, b64decode

flag_file = "flag.png"


def encrypt_image(image, key):
    perm_table = {0: (0, 1, 2), 1: (0, 2, 1), 2: (1, 0, 2), 3: (1, 2, 0), 4: (2, 0, 1), 5: (2, 1, 0)}
    size = image.size[0] * image.size[1]
    assert(size == len(key))
    pixels = list(image.getdata())
    
    for i in range(len(pixels)):
        p = pixels[i]
        kbyte = key[i]
        
        color = [p[i]^255 if kbyte & (1 << i) else p[i] for i in range(3)]  
        (r,g,b) = perm_table[int(kbyte) % 6]
        pixels[i] = (color[r], color[g], color[b])
 
    image.putdata(pixels)
    bs = BytesIO()
    image.save(bs, format=flag_file[-3:])

    return b64encode(bs.getvalue())



def handle():
    print("Dante took many pictures of his journey to the afterlife.")
    print("They contain many revelations. I give you one of these pictures if you give me one of yours!")

    answer = input("Do you accept the exchange [y/n]?")
    if answer == 'y':
        flag = Image.open(flag_file)
        key = get_random_bytes(flag.size[0] * flag.size[1])
    
        encrypted_flag = encrypt_image(flag, key)
        print(f"My picture:\n\n{encrypted_flag.decode()}\n\n")
    
        data = input("Your picture:")
        image = Image.frombytes(data=b64decode(data), mode=flag.mode, size=flag.size)
        encrypted_data = encrypt_image(image, key)
        print(f"This is for you:\n\n{encrypted_data.decode()}\n\n")
        print("Bye!")


if __name__ == '__main__':
    try:
        handle()
    except Exception:
        print("Something went wrong, bye!")
    