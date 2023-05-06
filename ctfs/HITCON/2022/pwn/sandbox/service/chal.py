#!/usr/bin/python3 -u

import atexit
import os
import random
import signal
import string
import subprocess
import sys
import tempfile

# Edit these variables for your own testing purpose
WWW_DIR = os.getenv("WWW")
WEB_HOST = os.getenv("HOST_IP")
WEB_PORT = os.getenv("PORT")
DOCKER_IMG_NAME = "hitcon2022_sandbox"

MAX_INPUT = 10 * 1024
TIMEOUT = 120

def handle_exit(*args):
    exit(0)

def timeout(signum, frame):
    print("TIMEOUT")
    handle_exit()

def init():
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(TIMEOUT)

def POW():
    from hashcash import check
    bits = 25
    resource = "".join(random.choice(string.ascii_lowercase) for i in range(8))
    print("[POW] Please execute the following command and submit the hashcash token:")
    print("hashcash -mb{} {}".format(bits, resource))
    print("( You can install hashcash with \"sudo apt-get install hashcash\" )")
    print("hashcash token: ", end='')
    sys.stdout.flush()

    stamp = sys.stdin.readline().strip()

    if not stamp.startswith("1:"):
        print("Only hashcash v1 supported")
        return False

    if not check(stamp, resource=resource, bits=bits):
        print("Invalid")
        return False

    return True

def main():
    size = None
    try:
        print(f"Your HTML file size: ( MAX: {MAX_INPUT} bytes ) ", end='')
        size = int(sys.stdin.readline())
    except:
        print("Not a valid size !")
        return

    if size > MAX_INPUT:
        print("Too large !")
        return

    print("Input your HTML file:")
    html = sys.stdin.read(size)

    tmp = tempfile.mkdtemp(dir=WWW_DIR, prefix=bytes.hex(os.urandom(8)))
    index_path = os.path.join(tmp, "index.html")
    with open(index_path, "w") as f:
        f.write(html)

    url = f"http://{WEB_HOST}:{WEB_PORT}/{os.path.basename(tmp)}/index.html"
    cmd = f"docker run --rm --privileged {DOCKER_IMG_NAME} {url}"
    try:
        subprocess.check_call(cmd, stderr=sys.stdout, shell=True)
    except subprocess.CalledProcessError as e:
        print("Execution error:")
        print(f"Return code: {e.returncode}")

if __name__ == '__main__':
    try:
        init()
        if POW():
            main()
        else:
            print("POW failed !")
    except Exception as e:
        pass
