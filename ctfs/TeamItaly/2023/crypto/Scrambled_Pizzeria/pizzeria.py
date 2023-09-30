#!/usr/bin/python3

import numpy as np
import numpy.typing as npt
from PIL import Image
import os


def permutation(
    img: npt.NDArray[np.uint8], c: npt.NDArray[np.uint64]
) -> npt.NDArray[np.uint8]:
    height, width = img.shape
    cm = c[np.arange(max(height, width)) % len(c)]
    rows = np.argsort(cm[:height])
    cols = np.argsort(cm[:width])
    return img[rows, :][:, cols]


def substitution(
    con: npt.NDArray[np.uint8], c: npt.NDArray[np.uint64]
) -> npt.NDArray[np.uint8]:
    ids = np.arange(np.prod(con.shape)) % len(c)
    return con ^ (c % 256).astype(np.uint8)[ids].reshape(con.shape)


def main():
    c: npt.NDArray[np.uint64] = np.frombuffer(os.urandom(400 * 8), np.uint64)

    print(
        "Hi, I'm here to take your order! Can you give me an image of the type of pizza you want me to cook?"
    )
    height = input("What's the height of the image? ")
    width = input("What's the width of the image? ")
    img_hex = input("Now send me the image and I'll do the rest!\n")

    try:
        height = int(height)
        width = int(width)

        assert height <= 400 and width <= 400

        img: npt.NDArray[np.uint8] = np.array(
            Image.frombytes("L", (width, height), bytes.fromhex(img_hex))
        )
    except:
        print("Uh oh! You're trying to trick me? Out of my pizzeria!")
        exit()
    con = permutation(img, c)
    enc = substitution(con, c)

    print("Oh mamma mia! I've scrambled all of your ingredients, look!")
    print(enc.tobytes().hex())

    flag_img: npt.NDArray[np.uint8] = np.array(Image.open("flag.jpg").convert("L"))
    flag_con = permutation(flag_img, c)
    flag_enc = substitution(flag_con, c)

    print("What a disaster! To make it up to me, here's a gift...")
    print(flag_enc.tobytes().hex())

    print("My job here is done!")


if __name__ == "__main__":
    main()
