#!/usr/bin/env -S python3 -u

import os
import subprocess as sp
from textwrap import dedent


def main():
    msg = dedent(
        """
        Enter assembly code
        Note: replace spaces with underscores, newlines with '|', e.g.,
          main:
            push 5
            call main
        becomes 'main:|push_5|call_main'
        """
    ).strip()
    print(msg)

    asm_code = input()

    input_path = "/tmp/input.asm"
    with open(input_path, "w") as f:
        f.write(asm_code.replace("_", " ").replace("|", "\n"))

    output_path = "/tmp/out.bin"

    p = sp.Popen(
        # Adjust path if running locally
        ["/app/stackception-asm", input_path, output_path],
        stdin=sp.DEVNULL,
        stdout=sp.DEVNULL,
        stderr=sp.PIPE,
    )

    p.wait(timeout=5)
    if p.returncode != 0:
        print("Assembly failed:")
        _, stderr = p.communicate()
        print(stderr.decode())
        exit(1)

    # Adjust path if running locally
    os.execv("/app/stackception", ["/app/stackception", output_path])


if __name__ == "__main__":
    main()
