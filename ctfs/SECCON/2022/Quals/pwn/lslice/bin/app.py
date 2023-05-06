#!/usr/bin/env python3
import subprocess
import sys
import tempfile

print("Input your Lua code (End with \"__EOF__\"):", flush=True)

source = ""
while True:
    line = sys.stdin.readline()
    if line.startswith("__EOF__"):
        break
    source += line

    if len(source) >= 0x2000:
        print("[-] Code too long")
        exit(1)

with tempfile.NamedTemporaryFile(suffix='.lua') as f:
    f.write(source.encode())
    f.flush()

    try:
        subprocess.run(["./lua", f.name],
                       stdin=subprocess.DEVNULL,
                       stdout=1, # mercy
                       stderr=subprocess.DEVNULL)
    except Exception as e:
        print("[-]", e)
    else:
        print("[+] Done!")
