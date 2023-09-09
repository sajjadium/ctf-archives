#!/usr/bin/env python3

import string
import random
import time
import math
import signal
import sys
from functools import partial

NUM_TO_SEND = 300
SEND_TIME = 15
GRACE_TIME = 120
FLAG = "./flag.txt"

# For better functionality when paired with socat
print_flush = partial(print, flush=True)

# Signal handler for program termination
def handler(signum, frame):
    print_flush("BOOM!")
    exit()

# Encrypt a mesage using a given key
def encrypt(key, message):
    return "".join(key.get(x, '') for x in message)

# Send a random status encrypted with a key
def send_status(key, initials):
    person = random.choice(initials)
    status = ''.join(random.choices(string.ascii_uppercase, k=4))
    print_flush(encrypt(key, f"{person}{status}"))

# Open the flag and print it
def print_flag():
    with open(FLAG, 'r') as f:
        data = f.read()
    print_flush(data)

def main(key, initials):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(GRACE_TIME)

    directors_initials = initials[0]

    sends_per_sec = NUM_TO_SEND / SEND_TIME
    start = time.time()
    elapsed, sent = 0, 0
    while elapsed < SEND_TIME:
        goal = math.ceil(elapsed * sends_per_sec)

        if goal == sent:
            time.sleep(1 / sends_per_sec)

        for idx in range(sent, goal):
            send_status(key, initials)
            sent += 1

        elapsed = time.time() - start

    print_flush("!!! ALERT !!!")
    print_flush("CRITICAL SYSTEM FAILURE")
    print_flush("UNABLE TO COMMUNICATE WITH ROCKET")
    print_flush("Help us land the rocket by using the director's initials:")
    print_flush(f"{directors_initials}")

    response = sys.stdin.read(7)
    if response != encrypt(key, f"{directors_initials}LAND"):
        print_flush("Uh oh..")
        return

    print_flag()


if __name__ == "__main__":
    key = list(string.ascii_uppercase)
    value = list(key)
    random.shuffle(value)
    lookup = dict(zip(key, value))

    with open('./initials.txt', 'r') as f:
        initials = f.read().strip().split('\n')

    main(lookup, initials)
