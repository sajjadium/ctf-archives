#!/usr/bin/env python3

import os
import sys
import tempfile

print("Enter exploit followed by EOF: ")
sys.stdout.flush()

buf = ""
while "EOF" not in buf:
    buf += input() + "\n"

with tempfile.TemporaryDirectory() as dir:
    os.chdir(dir)
    with open("exploit.html", 'w') as f:
        f.write("<script src='exploit.js'></script>")
    with open("exploit.js", 'w') as f:
        f.write(buf[:-3])
    os.environ["MOZ_DISABLE_CONTENT_SANDBOX"] = "1"
    os.system(f"timeout 20s /app/firefox/firefox --headless exploit.html")
