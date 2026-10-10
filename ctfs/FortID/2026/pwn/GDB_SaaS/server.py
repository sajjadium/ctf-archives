#!/usr/bin/python3

import base64
import os
import shutil
import signal
import subprocess
import tempfile

BAD_CHARS = set(
    "\x00\r\n"
    "\t"
    ";|&"
    "`$"
    "<>"
    "\\'\""
    "!"
    "#"
    ","
    "()[]{}"
)

def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    myprint("Time out!")
    exit(0)


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)

    myprint("Enter ELF bytes (base64): ")
    contents = input()

    if len(contents) >= 30*1024:
        myprint("ELF too large.\n")
        exit(0)

    try:
        data = base64.b64decode(contents)
    except Exception as e:
        myprint("Error decoding contents ({}).\n".format(e))
        exit(0)

    myprint("Enter function name: ")
    function_name = input()

    if len(function_name) >= 30 or any(c in BAD_CHARS for c in function_name):
        myprint("Invalid function name.\n")
        exit(0)

    tmp_dir = tempfile.mkdtemp(dir=".")
    shutil.copy("flag.txt", os.path.join(tmp_dir, "flag.txt"))

    tmp_path = os.path.join(tmp_dir, "a.out")
    with open(tmp_path, "wb") as tmp_file:
        tmp_file.write(data)

    os.chmod(tmp_path, 0o755)

    cmd = ["gdb", "-ex", f"disassemble {function_name}", "-ex", "quit", tmp_path]
    result = subprocess.check_output(cmd)
    myprint(result.decode('utf-8'))


if __name__ == "__main__":
    main()
