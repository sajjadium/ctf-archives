#!/usr/bin/env python3.7
import os
import random
import signal
import subprocess
import sys

def jsc(code):
    try:
        path = f'/tmp/exploit-{random.randrange(0, 1<<128):032x}.js'
        with open(path, "w") as f:
            f.write(code)
        subprocess.run(["./jsc", path], timeout=10)
    except Exception as e:
        print("[-] Execution Error", flush=True)
        print(e, flush=True)
        exit(1)
    finally:
        os.remove(path)

if __name__ == '__main__':
    signal.alarm(60)
    print("Send your javascript code here: (Close stdin to quit input)", flush=True)
    try:
        code = ''.join(sys.stdin.readlines())
        assert len(code) < 10000
        sys.stdin.close()
    except Exception as e:
        print("[-] Input Error", flush=True)
        print(e, flush=True)
        exit(1)

    try:
        jsc(code)
    except Exception as e:
        print("[-] Unknown Error", flush=True)
        print(e, flush=True)
        exit(1)
