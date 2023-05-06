#!/usr/bin/python3 -u
import random
import signal
import string
import subprocess
import sys

def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

def check_pow(bits):
    r = random_string(10)
    print(f"hashcash -mb{bits} {r}")
    solution = input("Solution: \n").strip()
    if subprocess.call(["hashcash", f"-cdb{bits}", "-r", r, solution],
                       cwd="/tmp",
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL) != 0:
        raise Exception("Invalid PoW")

check_pow(25)

port = random.randint(1024, 65535)
print(f"IPMI over lan will be listening on port {port}\n")

subprocess.call(["./qemu-system-arm",
                 "-monitor", "/dev/null",
                 "-m", "128M",
                 "-M", "romulus-bmc",
                 "-drive", "file=./content,format=raw,if=mtd,readonly",
                 "-net", "nic",
                 "-net", f"user,hostfwd=udp::{port}-:623",
                 "-nographic"], stdin=subprocess.DEVNULL, timeout=200)
