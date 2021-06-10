import random #pow
import subprocess #pow
import string #pow

POW_BITS = 25
def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
def check_pow():
    r = random_string(10)
    print(f"hashcash -mb{POW_BITS} {r}")
    solution = input("Solution:").strip()
    if subprocess.call(["hashcash", f"-cdb{POW_BITS}", "-r", r, solution],
                       cwd="/tmp",
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL) != 0:
        raise Exception("Invalid PoW")

