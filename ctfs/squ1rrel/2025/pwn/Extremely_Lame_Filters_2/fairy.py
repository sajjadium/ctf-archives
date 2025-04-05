#!/usr/bin/python3

from elf import *
from base64 import b64decode

data = b64decode(input("I'm a little fairy and I will trust any ELF that comes by!! (almost any)"))
elf = parse(data)

if elf.header.e_type != constants.ET_EXEC:
    print("!!")
    exit(1)

for segment in elf.segments:
    if segment.p_flags & SegmentFlags.X:
        content = elf.content(segment)
        for byte in content:
            if byte != 0:
                print(">:(")
                exit(1)

elf.run()
