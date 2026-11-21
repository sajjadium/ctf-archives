#!/usr/bin/env python3

import os
import sys
import code

DEBUG = os.environ.get("DEBUG", "0") == "1"

cpipe = os.fdopen(int(sys.argv[1]), "w", buffering=1)
devnull = open("/dev/null", mode="w")

print("""
Welcome to silent-snake, the blind REPL!

You've got a single ls that you can redeem using
`run_command('ls <directory_to_ls>')`

To exit the jail, use `exit()` or `run_command('exit')`

Have fun!
""")

if not DEBUG:
    sys.stdout.close()
    sys.stderr.close()
    os.close(1)
    os.close(2)
    sys.stdout = devnull
    sys.stderr = devnull

else:
    print(50*"=")
    print("WARNING: Debugging mode is *ON*. stdout and stderr are available here, but you won't be able to see the REPL's output during the challenge.")
    print(50*"=")

    # Redirect stderr to stdout
    os.dup2(1, 2, inheritable=True)

def run_command(cmd: str):
    cpipe.write(cmd + "\n")

code.interact(local=locals())

run_command("exit")
