#!/usr/bin/python3
import subprocess
import os
import pty
import base64


recipe = input("Give me your favourite macrowave cooking recipe! ")
filename = f"/tmp/recipe-{os.urandom(32).hex()}.org"
with open(filename, "wb") as f:
    f.write(base64.b64decode(recipe))

m, s = pty.openpty()
subprocess.run(["timeout", "15", "emacs", "-q", "-l", "./config.el", "-nw",  filename],
               stdin=s,
               stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL)
