import base64
import binascii
from pwn import *
import sys
import os


def main():
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

    fn = os.urandom(16).hex()
    fpath = f"attempts/{fn}"
    with open(fpath, "wb") as f:
        f.write(js)
        f.seek(0)

        try:
            p = process(["./js", fpath])
            p.interactive()
            sys.stdout.flush()
        except Exception as e:
            print(e, flush=True)


if __name__ == "__main__":
    main()
