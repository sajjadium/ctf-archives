#!/usr/bin/env python3

from icicle import *
from PIL import Image

def iii_to_png(fname):
    assert fname[-4:] == ".iii"
    iii = open(fname, 'rb').read()
    assert iii[:4] == b"\x7fIiI"
    iii = iii[4:]
    w = bytes_to_long(iii[:2])
    h = bytes_to_long(iii[2:4])
    iii = iii[4:]
    assert len(iii)%3 == 0
    png = Image.new("RGB", (w, h))
    for i in range(0, len(iii), 3):
        idx = i//3
        png.putpixel((idx//h, idx%h), (iii[i], iii[i+1], iii[i+2]))
    png.save(fname[:-4] + ".png")


def png_to_iii(fname):
    assert fname[-4:] == ".png"
    png = Image.open(fname)
    png = png.convert("RGB")
    out = b'\x7fIiI'
    outfile = fname[:-4]+'.iii'
    outfile = open(outfile, "wb")
    w, h = png.size
    out += bytes([(w>>8)&0xff])
    out += bytes([w&0xff])
    out += bytes([(h>>8)&0xff])
    out += bytes([h&0xff])
    for x in range(w):
        for y in range(h):
            rgb = png.getpixel((x, y))
            for color in rgb:
                out += bytes([color])
    outfile.write(out)
    outfile.close()

def hide_data(fname, data):
    assert fname[-4:] == ".iii"
    vm = VM(program=open("stego.s").read(), testing=1, inp=[fname, data], limit=9999)
    vm.run()    
    print(vm.output_buffer)

def main():
    print("Welcome to the ICICLE Image Interchange!")
    print()
    print("1) Convert png to iii")
    print("2) Convert iii to png")
    print("3) Encrypt data in iii file")
    print()
    inp = input('>>> ')
    if '1' in inp:
        png_to_iii(input("Enter filename: "))
    elif '2' in inp:
        iii_to_png(input('Enter filename: '))
    elif '3' in inp:
        hide_data(input("Enter image filename: "), input("Enter flag: "))

if __name__ == '__main__':
    main()
    