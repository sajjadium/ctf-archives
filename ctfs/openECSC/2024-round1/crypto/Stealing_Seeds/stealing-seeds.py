#!/usr/bin/env python3

import os
import signal
import random
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from hashlib import sha256

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("openECSC{"))
assert(FLAG.endswith("}"))

def main():

    seed_size = 256
    seed = getPrime(seed_size)

    # Just to protect my seed
    k = random.randint(1, 2**seed_size - 1)

    print("""I have my seed, if you give me yours we can generate some random numbers together!
Just don't try to steal mine...
""")

    while True:
        choice = int(input("""Which random do you want to use?
1) Secure
2) Even more secure
3) That's enough
> """))
        if choice not in [1, 2, 3]:
            print("We don't have that :(")
            continue
        if choice == 3:
            break
        user_seed = int(
            input("Give me your seed: "))
        if user_seed.bit_length() > seed_size:
            print(
                f"Your seed can be at most {seed_size} bits!")
            continue
        if choice == 1:
            final_seed = ((seed ^ user_seed) +
                           seed) ^ k
        else:
            final_seed = ((seed + user_seed) ^
                           seed) ^ k

        random_number = bytes_to_long(sha256(long_to_bytes(final_seed)).digest())

        print(f"Random number:", random_number)
    
    guess = int(input("Hey, did you steal my seed? "))

    if guess == seed:
        print(FLAG)
    else:
        print("Ok, I trust you")
    return


def handler(signum, frame):
    print("Time over!")
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    main()