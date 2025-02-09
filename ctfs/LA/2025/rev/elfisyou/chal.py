#!/usr/local/bin/python

import os
import sys
import tty

N = 13

elf = open("elf", "rb").read().ljust(N*N, b"\x00")
grid = [list(elf[i:i + N]) for i in range(0, len(elf), N)]

x, y = N-1, 0

def view(clear=True):
    print("\x1b[2J")
    print("="*38, end="\r\n")
    print("| byte is push".ljust(37)+"|", end="\r\n")
    print("|            flag.txt is win".ljust(37)+"|", end="\r\n")
    print("|                         elf is you".ljust(37)+"|", end="\r\n")
    print("="*38, end="\r\n")
    for i in range(N):
        for j in range(N):
            a = ""
            b = " "
            c = hex(grid[i][j])[2:4].rjust(2, "0")
            if (i, j) == (y, x):
                a = "\x1b[48;5;10m"
                b = "\x1b[0m" + b
                c = "##"
            elif grid[i][j] != 0:
                a = "\x1b[48;5;9m"
                b = "\x1b[0m" + b
            print(a+c+b, end="")
        print("\r")
    sys.stdout.flush()

def push(d):
    global x, y
    if not d:
        return False
    dx = d[0]
    dy = d[1]
    nx, ny = x+dx, y+dy
    while nx in range(N) and ny in range(N):
        if grid[ny][nx] == 0:
            break
        nx += dx
        ny += dy
    else:
        return False
    xx, yy = nx, ny
    while xx != x or yy != y:
        grid[yy][xx] = grid[yy-dy][xx-dx]
        xx -= dx
        yy -= dy
    x += dx
    y += dy
    return True

view(0)
if sys.stdin.isatty():
    tty.setcbreak(0)
while True:
    try:
        c = sys.stdin.read(1)
        if c == "x":
            path = "/tmp/elf"
            elf = b"".join(bytes(x) for x in grid)
            with open(path, "wb") as file:
                file.write(elf)
                file.close()
            os.chmod(path, 0o700)
            os.execve(path, [path], {})
        elif c == "q":
            exit()
        d = {
            "s": (0, 1),
            "w": (0, -1),
            "a": (-1, 0),
            "d": (1, 0),
        }.get(c.lower())
        if push(d):
            view()
    except EOFError:
        pass
