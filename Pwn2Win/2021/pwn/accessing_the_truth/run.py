#!/usr/bin/python3 -u
import random
import string
import subprocess
import tempfile

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

fname = tempfile.NamedTemporaryFile().name

subprocess.call(["cp", "OVMF.fd", fname])
try:
  subprocess.call(["chmod", "u+w", fname])
  subprocess.call(["qemu-system-x86_64",
                   "-monitor", "/dev/null",
                   "-m", "64M",
                   "-drive", "if=pflash,format=raw,file=" + fname, 
                   "-drive", "file=fat:rw:contents,format=raw",
                   "-net", "none",
                   "-nographic"], stderr=subprocess.DEVNULL, timeout=60)
except:
  pass

subprocess.call(["rm", "-rf", fname])
print("Bye!")
