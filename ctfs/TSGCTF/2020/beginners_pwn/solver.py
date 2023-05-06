# I'm sorry I am using Python2 :( for pwning
from __future__ import division, print_function
import random
# Run: pip install pwntools
from pwn import *
import argparse
import time


# A way to start the program server locally, and debug your exploit on Linux.
# 1. Install socat
# 2. socat TCP-L:3001,reuseaddr,fork EXEC:./beginners_pwn
# 3. python solver.py
# 4. sudo gdb -q -p `pgrep beginners_pwn`

host = "localhost"
port = 3001

r = remote(host, port)

print('Enter `newline` to start the exploit')
raw_input()

#### write your exploit here. ####
r.sendline('AAAA') # dummy: send `AAAA' to the server

# r.interactive() # After you get shell, you can intereact with the server!

