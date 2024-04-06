#!/usr/local/bin/python3

from tempfile import NamedTemporaryFile, TemporaryDirectory
from os import urandom, system, mkdir
from string import printable
from pathlib import Path
from shutil import copy

blacklist = [
    "cInclude",
    "embedFile",
]
character_whitelist = printable

def err(code: int, msg: str):
    print(msg)
    exit(code)

def check(leftover: str):
    for disallow in blacklist:
        if leftover.startswith(disallow):
            err(1, "blacklisted directive found")

def round():
    with TemporaryDirectory() as cache:
        cache = Path(cache)
        with NamedTemporaryFile("w", suffix=".zig", dir=cache) as zig:
            zig.write(src)
            zig.flush()

            cmd = f"/app/zig/zig build-exe -fno-emit-bin -fsingle-threaded -fno-lto -fno-PIC --no-gc-sections --cache-dir {cache} --global-cache-dir /tmp {zig.name}"
            system(cmd)

limit = 1337
src = ""
print("code: ")
while True:
    line = input()
    assert all([ch in character_whitelist for ch in line]), "character not in whitelist"
    if line.startswith("EOF"):
        break
    src += line + "\n"
    overflow = len(src) - limit
    if overflow > 0:
        suffix = "s" if overflow > 1 else ""
        err(1, f"input too long by {overflow} byte{suffix}")

for i in range(len(src)):
    if src[i] == '@':
        check(src[i+1:])

round()
