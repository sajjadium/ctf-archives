#!/usr/bin/python3
import io
import os
import sys

flag = os.environb.get(b"FLAG")
if not flag:
    flag = b"flag{fake_flag}"

def readline(fd):
    buf = []
    while True:
        c = os.read(fd, 1)
        if c == b"\n":
            break
        buf.append(c)
    return b"".join(buf)


# use virtual serial line for communication
fd = os.open(sys.argv[1], os.O_RDWR | os.O_NOCTTY)

while True:
    command = readline(fd)
    print("got command:", command)
    if b"coffe" in command:
        # got the command, confirm the order
        os.write(fd, b"Here it comes: " + flag + b"\n")
