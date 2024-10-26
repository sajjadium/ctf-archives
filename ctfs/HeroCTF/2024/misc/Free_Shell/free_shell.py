#!/usr/bin/env python3
import os
import subprocess


print("Welcome to the free shell service!")
print("Your goal is to obtain a shell.")

command = [
    "/bin/sh",
    input("Choose param: "),
    os.urandom(32).hex(),
    os.urandom(32).hex(),
    os.urandom(32).hex()
]
subprocess.run(command)