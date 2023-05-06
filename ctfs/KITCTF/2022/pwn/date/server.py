import tempfile
import signal
import base64
import binascii
from pwn import *
import sys


def handler(signum, frame):
    raise OSError("Wakeup")


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(60)

    try:
        b64 = input("Base64 encoded file: ").strip()
    except EOFError:
        return

    try:
        js = base64.b64decode(b64)
    except binascii.Error:
        print("Invalid input", flush=True)
        return

    if len(js) >= 50000:
        print("Invalid input", flush=True)
        return
        
    with tempfile.NamedTemporaryFile() as f:
        f.write(js)
        f.seek(0)

        try:
            # no jit/wasm for you :)
            p = process(["./d8", "--jitless", "--no-expose-wasm", f.name])
            p.interactive()
            sys.stdout.flush()
        except Exception as e:
            print(e, flush=True)


if __name__ == "__main__":
    main()
