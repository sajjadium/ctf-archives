#!/usr/local/bin/python

import ctypes
import mmap
import sys

flag = "redacted"

print("White House declared Python to be memory safe :tm:")

buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
ftype = ctypes.CFUNCTYPE(ctypes.c_void_p)
fpointer = ctypes.c_void_p.from_buffer(buf)
f = ftype(ctypes.addressof(fpointer))

u_can_do_it = bytes.fromhex(input("So enter whatever you want 👍 (in hex): "))

buf.write(u_can_do_it)

f()

del fpointer
buf.close()

print("byebye")
