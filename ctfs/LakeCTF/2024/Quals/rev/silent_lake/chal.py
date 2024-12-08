#!/usr/bin/env python3

import subprocess
import tempfile
import os

def pns(s: str) -> None:
    print(s)

pns("Give me the correct source code.")
source = ""
for line in iter(input, "EOF"):
    source += line + "\n"

with tempfile.TemporaryDirectory() as tmpdirname:
    with open(os.path.join(tmpdirname, "main.c"), "w") as f:
        f.write(source)
    subprocess.run(["/codeql/codeql",
                    "database",
                    "create",
                    "--language=c", 
                    "--command=clang -nostdinc -O0 -o " + os.path.join(tmpdirname, "main") + " " + os.path.join(tmpdirname, "main.c"),
                    os.path.join(tmpdirname, "db")],
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                   )
    
    result = subprocess.run(["/codeql/codeql",
                    "query",
                    "run",
                    "vscode-codeql-starter/codeql-custom-queries-cpp/example.ql",
                    "-d",
                    os.path.join(tmpdirname, "db")],
                   capture_output = True, text=True)
    print(result.stdout)
    if "correct" in result.stdout:
        try:
            with open("/flag.txt", "r") as f:
                print(f.read())
        except:
            print("EPFL{local_fake_flag}")
