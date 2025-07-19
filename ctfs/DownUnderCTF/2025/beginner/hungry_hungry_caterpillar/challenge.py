#!/usr/bin/env python3

import os


def xor(a, b):
    return bytes(left ^ right for left, right in zip(a, b))


def main():
    flag = open("flag.txt", "rb").read()
    assert flag[1] == ord("U")
    flag += os.urandom(len(flag) * 6)
    keystream = os.urandom(len(flag))

    print(
        f"""
        In the light of the moon a little egg lay on a leaf.

        One Sunday morning the warm sun came up and - pop! - out of the egg
        came a tiny and very hungry caterpillar.

        ( drawing of the sun :D )

        He started to look for some food.

        On Monday he ate through one apple. But he was still hungry.

        {xor(flag[::1], keystream).hex()}

        On Tuesday he ate through two pears, but he was still hungry.

        {xor(flag[::2], keystream).hex()}

        On Wednesday he ate through three plums, but he was still hungry.

        {xor(flag[::3], keystream).hex()}

        On Thursday he ate through four strawberries, but he was still hungry.

        {xor(flag[::4], keystream).hex()}

        On Friday he ate through five oranges, but he was still hungry.

        {xor(flag[::5], keystream).hex()}

        On Saturday he ate through one piece of chocolate cake, one ice-cream
        cone, one pickle, one slice of Swiss cheese, one slice of salami, one
        lollipop, one piece of cherry pie, one sausage, one cupcake, and one
        slice of watermelon.

        {xor(flag[::6], keystream).hex()}

        That night he had a stomachache!

        ( drawing of a leaf ~~ )

        The next day was Sunday again. The caterpillar ate through one nice
        green leaf, and after that he felt much better.

        {xor(flag[::7], keystream).hex()}

        Now he wasn't hungry any more - and he wasn't a little caterpillar any
        more. He was a big fat caterpillar :<

        He built a small house, called a cocoon, around himself. He stayed
        inside for more than two weeks. Then he nibbled a hole in the cocoon,
        pushed his way out and ...

        he was a beautiful butterfly!
        """
    )


if __name__ == "__main__":
    main()
