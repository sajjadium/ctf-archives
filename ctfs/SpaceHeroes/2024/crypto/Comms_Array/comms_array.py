#!/use/bin/env python3
import os, sys, zlib, fcntl

flag = os.getenvb(b'FLAG', b'UNSET')

size = sys.stdin.buffer.read(1)
size = size[0] if size else 0

flags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, flags | os.O_NONBLOCK)

max_sz = 255 - len(flag)
buf = sys.stdin.buffer.read(min(size, max_sz))
buf = buf if buf else b''
buf = buf.ljust(max_sz, b'\x00') + flag

calc_crc = zlib.crc32(buf[:size])
if calc_crc == 0:
    print("yup")
