#!/usr/bin/env python3

import os
import subprocess
import base64

def main():
    print("This challenge is derived from a real world example, no joke")
    print("Anyway: Encode and exploit this")

    try:
        inp = input("Give input plox: ")
        inp = inp.upper()

        decoded = base64.b64decode(inp).lower()
        open("/tmp/inp", "wb").write(decoded)

        print(subprocess.check_output("/bin/bash < /tmp/inp", shell=True))
    except Exception as e:
        print("Something went wrong. Bye!")

if __name__ == "__main__":
    main()
