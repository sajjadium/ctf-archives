#!/usr/bin/env python3

import os
import sys
from os.path import isfile, abspath, dirname, join


# This script simulates what's going on the server. Qemu is launched exactly as
# shown below. The bios-template is exaclty the one used on the server.


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <shellcode_fp>')
        sys.exit(1)

    shellcode_fp = abspath(sys.argv[1])
    floppy_img_fp = abspath(join(dirname(__file__), 'floppy-dummy-flag.img'))
    bios_template_fp = abspath(join(dirname(__file__), 'bios-template.bin'))
    bios_patched_fp = abspath(join(dirname(__file__), 'bios-patched.bin'))

    assert isfile(shellcode_fp)
    assert isfile(floppy_img_fp)
    assert isfile(bios_template_fp)
    if isfile(bios_patched_fp): os.unlink(bios_patched_fp)

    with open(bios_template_fp, 'rb') as f:
        bios = bytearray(f.read())

    with open(shellcode_fp, 'rb') as f:
        sc = f.read()
        assert len(sc) <= 0x800

    x_idx = bios.find(b'X' * 0x800)
    assert x_idx >= 0

    bios[x_idx:x_idx+len(sc)] = sc

    with open(bios_patched_fp, 'wb') as f:
        f.write(bios)

    run_qemu(bios_patched_fp, floppy_img_fp)


def run_qemu(bios_fp, floppy_fp):
    cmd = f'qemu-system-i386 -drive format=raw,if=floppy,media=disk,file={floppy_fp} -bios {bios_fp} -net none -cpu base -monitor none -snapshot -no-reboot -sandbox on,obsolete=deny,elevateprivileges=deny,spawn=deny,resourcecontrol=deny -curses'
    os.system(cmd)


if __name__ == '__main__':
    main()
