#!/usr/bin/python3 -u
# (script from hitcon..)
import atexit
import os
import random
import signal
import string
import subprocess
import sys
import tempfile

MAX_INPUT = 100 * 1024
TIMEOUT = 120
JSC_PATH = "/home/user/jsc"
LIB_PATH = "/home/user/lib/"

def main():
    size = None
    try:
        print(f"Your js file size: ( MAX: {MAX_INPUT} bytes ) ", end='')
        size = int(sys.stdin.readline())
    except:
        print("Not a valid size !")
        return

    if size > MAX_INPUT:
        print("Too large !")
        return

    print("Input your js file:")
    src = sys.stdin.read(size)

    tmp = tempfile.mkdtemp(dir="/tmp", prefix=bytes.hex(os.urandom(8)))
    full_path = os.path.join(tmp, "exp.js")
    with open(full_path, "w") as f:
        f.write(src)

    
    cmd = f"LD_LIBRARY_PATH={LIB_PATH} {JSC_PATH} {full_path}"
    try:
        subprocess.check_call(cmd, stderr=sys.stdout, shell=True)
    except subprocess.CalledProcessError as e:
        print("Execution error:")
        print(f"Return code: {e.returncode}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
