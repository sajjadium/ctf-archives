#!/usr/local/bin/python3

from tempfile import NamedTemporaryFile, TemporaryDirectory
from subprocess import run
from os import urandom
from string import ascii_letters, digits, punctuation

whitelist = [
    "import",
    "bitSizeOf",
    "sizeOf",
    "compileError",
    "TypeOf",
    "popCount",
    "clz",
    "ctz",
    "as",
    "intCast",
    "truncate",
    "enumFromInt",
    "floatCast",
    "floatFromInt",
    "intFromBool",
    "intFromFloat",
    "intFromEnum",
    "intFromError",
    "bitCast"
]
character_whitelist = " \n\r" + ascii_letters + digits + punctuation

def err(code: int, msg: str):
    print(msg)
    exit(code)

def check(leftover: str):
    for allow in whitelist:
        if leftover.startswith(allow):
            return

    err(1, f"bad directive found: {leftover}")

def round():
    size = 1337 + urandom(1)[0]
    victim = list(urandom(size))

    with NamedTemporaryFile("w", suffix=".zig") as zig:
        repl = str(victim)[1:-1]
        repl = f"var input = [_]u8{{ {repl} }};"
        repl = src.replace("var input = [0]u8{};", repl, 1)
        zig.write(repl)
        zig.flush()

        with TemporaryDirectory() as cache:
            print("compiling...")
            handle = run(["/app/zig/zig", "build-exe", "-fno-emit-bin", "--cache-dir", cache, "--global-cache-dir", cache, zig.name], capture_output=True)

    if handle.returncode != 0 and handle.returncode != 1:
        err(1, "stop crashing my compiler")

    output = f"{handle.stderr}\n{handle.stdout}"
    victim = bytes(sorted(victim)).hex()

    if victim in output:
        return
    else:
        err(1, "no")

limit = 4444
src = ""
print("code: ")
while True:
    line = ascii(input())[1:-1]
    assert all([ch in character_whitelist for ch in line]), "character not in whitelist"
    if line.startswith("EOF"):
        break
    src += line + "\n"
    if len(src) >= limit:
        err(1, f"input too long by {len(src) - limit} bytes")

for i in range(len(src)):
    if src[i] == '@':
        check(src[i+1:])

round()

print(open("flag.txt", "r").read())