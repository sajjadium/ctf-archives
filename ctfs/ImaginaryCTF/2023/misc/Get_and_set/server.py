#!/usr/bin/env python3
import pydash


class Dummy:
    pass


if __name__ == "__main__":
    obj = Dummy()
    while True:
        src = input("src: ")
        dst = input("dst: ")
        pydash.set_(obj, dst, pydash.get(obj, src))
