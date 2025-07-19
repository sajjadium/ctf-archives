#!/usr/bin/env python3

import ctypes

obj = {}
print(f"addrof(obj) = {hex(id(obj))}")

libc = ctypes.CDLL(None)
system = ctypes.cast(libc.system, ctypes.c_void_p).value
print(f"system = {hex(system or 0)}")

fakeobj_data = bytes.fromhex(input("fakeobj: "))
for i in range(72):
    ctypes.cast(id(obj), ctypes.POINTER(ctypes.c_char))[i] = fakeobj_data[i]

print(obj)
