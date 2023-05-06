#!/usr/bin/env python3

import cext as module
from binascii import unhexlify

MAXSIZE = 0x50

class CBytes:
    def __init__(self, size):
        b = module.input(size)
        self.b = b

    def __len__(self):
        return module.len(self.b)

    def print(self):
        return module.print(self.b)

def getsize(maxsize=MAXSIZE):
    size = int(input("Enter size: "))
    assert(size < maxsize)
    return size

def menu():
    print("1. Input")
    print("2. Length")
    print("3. Print")
    print("0. Exit")

if __name__ == "__main__":
    size = getsize()
    cb = CBytes(size)
    choice = -1
    while choice != 0:
        menu()
        choice = int(input("Choice: "))
        if choice == 1:
            size = getsize()
            cb = CBytes(size)
        elif choice == 2:
            l = len(cb)
            print(f"Length: {l}")
        elif choice == 3:
            cb.print()
