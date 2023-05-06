#!/usr/bin/env python3
import string
import ctypes
import os
import sys
import subprocess

ok_chars = string.ascii_uppercase + string.digits
elf_header = bytes.fromhex("7F454C46010101000000000000000000020003000100000000800408340000000000000000000000340020000200280000000000010000000010000000800408008004080010000000000100070000000000000051E5746400000000000000000000000000000000000000000600000004000000")

print("Welcome to EBCSIC!")
sc = input("Enter your alphanumeric shellcode: ")
try:
    assert all(c in ok_chars for c in sc)
    sc_raw = sc.encode("cp037")
    assert len(sc_raw) <= 4096
except Exception as e:
    print("Sorry, that shellcode is not acceptable.")
    exit(1)

print("Looks good! Let's try your shellcode...")
sys.stdout.flush()

memfd_create = ctypes.CDLL("libc.so.6").memfd_create
memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_int]
memfd_create.restype = ctypes.c_int

fd = memfd_create(b"prog", 0)
os.write(fd, elf_header)
os.lseek(fd, 4096, 0)
os.write(fd, sc_raw.ljust(4096, b"\xf4"))
os.execle("/proc/self/fd/%d" % fd, "prog", {})
