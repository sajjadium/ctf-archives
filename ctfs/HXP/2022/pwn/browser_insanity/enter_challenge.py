#!/usr/bin/python3

# This script is just for entering the URL into the browser in the VM.
#
# Accepted URL characters are: upper and lowercase ASCII, digits, .:/ %=

import time
import subprocess
import pty
import os
import string
import sys

data = input("What is the URL to visit? ")

if len(data) > 64:
    print("URL is too long", flush=True)
    exit(1)

allowed = string.ascii_lowercase + string.ascii_uppercase + string.digits + ".:/ %="
ok = all(ch in allowed for ch in data)
if ok == False:
    print("Input is invalid", flush=True)
    exit(1)

sys.stdin.close()

master, slave = pty.openpty()

run_vm = subprocess.Popen(["./run_vm.sh"], stdout=slave, stdin=slave, stderr=slave, text=True)
os.close(slave)

SLEEP_TIME_FOR_OS_BOOT = 12
SLEEP_TIME_FOR_CMD = .12
SLEEP_BEFORE_END = 10

def send_cmd(cmd):
    os.write(master, cmd + b"\n")
    time.sleep(SLEEP_TIME_FOR_CMD)

# Let's wait a bit.
print(f"Sleeping for {SLEEP_TIME_FOR_OS_BOOT} secs till VM boots", flush=True)

# Enter monitor with CTRL-a-c
send_cmd(b"\x01c")

time.sleep(1)
send_cmd(b"mouse_button 1")
send_cmd(b"mouse_button 2")
send_cmd(b"sendkey kp_enter")

time.sleep(SLEEP_TIME_FOR_OS_BOOT)

# Reposition cursor to address tab
for u in range(10):
    send_cmd(b"mouse_move 0 -20")

# click click
send_cmd(b"mouse_button 1")
send_cmd(b"mouse_button 2")

# erase
for u in range(20):
    send_cmd(b"sendkey backspace")

# type-in each character
for u in data:
    if u == ":":
        u = "shift-semicolon"
    elif u == ".":
        u = "dot"
    elif u == "/":
        u = "slash"
    elif u == " ":
        u = "spc"
    elif u == "%":
        u = "shift-5"
    elif u == "=":
        u = "equal"
    cmd = "sendkey " + u
    print(f"Sending: \"{cmd}\"", flush=True)
    send_cmd(cmd.encode("ascii"))

# ok, let's visit
send_cmd(b"sendkey kp_enter")

# Give some time for the webpage to be downloaded, etc.
print(f"Sleeping for {SLEEP_BEFORE_END} secs and exiting", flush=True)
time.sleep(SLEEP_BEFORE_END)

# This should have been enough, let's stop the vm.
run_vm.kill()
print("Bye", flush=True)

