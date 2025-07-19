#!/usr/bin/env python3

import ctypes

a = [{}, (), [], "", 0.0]
while True:
    try:
        inp = input("> ")
        cmd, idx, *val = inp.split()
        idx = int(idx)
        match cmd:
            case "r":
                print(a[idx])
            case "w":
                ctypes.cast(
                    id(a) + idx, ctypes.POINTER(ctypes.c_char)
                )[0] = int(val[0])
            case _:
                break
    except Exception as e:
        print("error:", e)
