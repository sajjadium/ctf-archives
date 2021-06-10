#!/usr/bin/python3 -u
import random
import string
import subprocess

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

try:
  subprocess.call(["sage", "chall.sage"], timeout=60*40)
except:
  pass

print("Bye!")
