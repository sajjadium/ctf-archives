import os
import struct

BITS = int(os.getenv("BITS", "64"))

FLAG = os.getenv("FLAG", "ALLES!{TESTFLAG}")

SEED = int.from_bytes(os.urandom(BITS//8), "little")

def rol(x, n, size): return ((x << n) | (x >> (size - n))) & (2**size)-1
def ror(x, n, size): return ((x >> n) | (x << (size - n))) & (2**size)-1

ROTATIONS = [3, 5]

def rng(x, size):
    v = x
    for i in ROTATIONS:
        v |= rol(x, i, size)
        v ^= ror(v, i, size)
    return v

def gen_random(seed, bits, mask):
    state = seed
    while True:
        state = rng(state, bits)
        yield state & mask

def main():
    print("Here are some random numbers, now guess the flag")
    rng = gen_random(SEED, BITS, 0xFF)
    for i in range(len(FLAG)):
        print(next(rng) ^ ord(FLAG[i]))

if __name__ == "__main__":
    main()